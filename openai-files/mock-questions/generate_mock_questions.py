#!/usr/bin/env python3
"""
Wikipedia MCQ Question Generator
Processes extracted Wikipedia JSON files and generates multiple-choice questions
using multiple OpenAI API keys for parallel processing.
"""

import json
import os
import sys
import time
import logging
import asyncio
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import argparse
from dataclasses import dataclass, asdict
from openai import OpenAI
from dotenv import load_dotenv
import threading
from queue import Queue, Empty

# Rich library for better console output (optional)
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.logging import RichHandler
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    class SimpleConsole:
        def print(self, text, **kwargs):
            print(text)
    console = SimpleConsole()
    RICH_AVAILABLE = False

@dataclass
class ProcessingStats:
    """Statistics for tracking MCQ generation progress"""
    total_files: int = 0
    completed_files: int = 0
    skipped_files: int = 0
    total_sections: int = 0
    completed_sections: int = 0
    total_bullet_points: int = 0
    completed_bullet_points: int = 0
    failed_bullet_points: int = 0
    total_questions_generated: int = 0
    start_time: Optional[str] = None
    last_update_time: Optional[str] = None
    api_keys_used: int = 0

@dataclass
class ProcessingState:
    """State information for resume functionality"""
    folder_path: str
    last_processed_file: Optional[str] = None
    last_processed_section: Optional[str] = None
    last_processed_bullet_point: Optional[int] = None
    timestamp: Optional[str] = None
    stats: ProcessingStats = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = ProcessingStats()

@dataclass
class BulletPointTask:
    """Represents a single bullet point processing task"""
    file_path: Path
    section_index: int
    bullet_point_index: int
    chapter_name: str
    section_name: str
    section_number: str
    bullet_point_text: str
    questions_per_point: int = 2

class APIKeyManager:
    """Manages multiple OpenAI API keys and their usage"""
    
    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.model_name = model_name
        self.api_keys = self.discover_api_keys()
        self.clients = self.initialize_clients()
        self.usage_stats = {key: 0 for key in self.api_keys}
        self.lock = threading.Lock()
        
    def discover_api_keys(self) -> List[str]:
        """Discover all available OpenAI API keys from environment"""
        api_keys = []
        
        # Check for primary key
        primary_key = os.getenv('OPENAI_API_KEY')
        if primary_key:
            api_keys.append(primary_key)
        
        # Check for numbered keys
        i = 1
        while True:
            key = os.getenv(f'OPENAI_API_KEY_{i}')
            if key:
                api_keys.append(key)
                i += 1
            else:
                break
        
        if not api_keys:
            raise ValueError("No OpenAI API keys found in environment variables")
        
        console.print(f"[green]✓ Discovered {len(api_keys)} API keys[/green]")
        return api_keys
    
    def initialize_clients(self) -> List[OpenAI]:
        """Initialize OpenAI clients for each API key"""
        clients = []
        for i, api_key in enumerate(self.api_keys):
            try:
                client = OpenAI(api_key=api_key)
                clients.append(client)
                console.print(f"[green]✓ Initialized client {i+1}/{len(self.api_keys)}[/green]")
            except Exception as e:
                console.print(f"[red]✗ Failed to initialize client {i+1}: {e}[/red]")
                raise
        return clients
    
    def get_next_client(self) -> Tuple[OpenAI, int]:
        """Get the next available client using round-robin"""
        with self.lock:
            # Find the client with least usage
            min_usage = min(self.usage_stats.values())
            for i, key in enumerate(self.api_keys):
                if self.usage_stats[key] == min_usage:
                    self.usage_stats[key] += 1
                    return self.clients[i], i
    
    def get_usage_stats(self) -> Dict[str, int]:
        """Get current usage statistics"""
        with self.lock:
            return self.usage_stats.copy()

class MCQGenerator:
    """
    Main MCQ generator class with multi-API key support
    """
    
    def __init__(self, folder_path: str, model_name: str = "gpt-4.1-mini", 
                 questions_per_point: int = 2, max_workers: int = None):
        self.folder_path = Path(folder_path)
        self.model_name = model_name
        self.questions_per_point = max(1, min(questions_per_point, 3))  # Limit 1-3
        
        # Initialize API key manager
        try:
            self.api_manager = APIKeyManager(model_name)
            console.print(f"[green]✓ Multi-API system initialized with {len(self.api_manager.api_keys)} keys[/green]")
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize API manager: {e}[/red]")
            sys.exit(1)
        
        # Set max workers (default to number of API keys * 2)
        self.max_workers = max_workers or min(len(self.api_manager.api_keys) * 2, 10)
        
        # Setup directories
        self.output_dir = self.folder_path.parent / "question_bank"
        self.logs_dir = self.output_dir / "logs"
        self.backups_dir = self.output_dir / "backups"
        
        for dir_path in [self.output_dir, self.logs_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Initialize state
        self.state_file = self.logs_dir / "mcq_generation_state.json"
        self.processing_state = self.load_processing_state()
        self.processing_state.stats.api_keys_used = len(self.api_manager.api_keys)
        
        # Thread-safe data structures
        self.processed_questions = {}  # file_path -> {section_index: {bullet_point_index: questions}}
        self.data_lock = threading.Lock()
        
        # Statistics
        self.start_time = datetime.now()
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Main logger
        self.logger = logging.getLogger('MCQGenerator')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handlers
        master_handler = logging.FileHandler(self.logs_dir / 'mcq_generation.log')
        master_handler.setFormatter(logging.Formatter(log_format))
        master_handler.setLevel(logging.INFO)
        
        question_handler = logging.FileHandler(self.logs_dir / 'question_generation.log')
        question_handler.setFormatter(logging.Formatter(log_format))
        question_handler.setLevel(logging.DEBUG)
        
        # Console handler
        if RICH_AVAILABLE:
            console_handler = RichHandler(console=console, rich_tracebacks=True)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        
        console_handler.setLevel(logging.INFO)
        
        # Add handlers
        self.logger.addHandler(master_handler)
        self.logger.addHandler(question_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("Multi-API MCQ generation system initialized")
    
    def load_processing_state(self) -> ProcessingState:
        """Load processing state from file or create new one"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state = ProcessingState(**data)
                    if 'stats' in data:
                        state.stats = ProcessingStats(**data['stats'])
                    self.logger.info(f"Loaded existing processing state from {self.state_file}")
                    return state
            except Exception as e:
                self.logger.warning(f"Failed to load processing state: {e}. Starting fresh.")
        
        # Create new state
        state = ProcessingState(folder_path=str(self.folder_path))
        state.stats.start_time = datetime.now().isoformat()
        self.logger.info("Created new processing state")
        return state
    
    def save_processing_state(self):
        """Save current processing state to file"""
        try:
            self.processing_state.timestamp = datetime.now().isoformat()
            self.processing_state.stats.last_update_time = datetime.now().isoformat()
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.processing_state), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save processing state: {e}")
    
    def discover_extracted_files(self) -> List[Path]:
        """Discover extracted JSON files in the input folder"""
        self.logger.info(f"Discovering extracted JSON files in {self.folder_path}")
        
        try:
            # Look for extracted files (priority) and flat dataset as fallback
            extracted_files = list(self.folder_path.glob("extracted_*.json"))
            if not extracted_files:
                flat_dataset = self.folder_path / "flat_dataset.json"
                if flat_dataset.exists():
                    extracted_files = [flat_dataset]
            
            self.logger.info(f"Discovered {len(extracted_files)} extracted files")
            self.processing_state.stats.total_files = len(extracted_files)
            return sorted(extracted_files)
        except Exception as e:
            self.logger.error(f"Failed to discover extracted files: {e}")
            return []
    
    def load_extracted_file(self, file_path: Path) -> Optional[Dict]:
        """Load and validate extracted JSON file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both individual extracted files and flat dataset
            if 'sections' in data:
                sections = data['sections']
            elif isinstance(data, list):
                sections = data
            else:
                self.logger.error(f"Invalid structure in {file_path}: expected sections or list")
                return None
            
            self.logger.debug(f"Loaded {len(sections)} sections from {file_path}")
            return {'sections': sections, 'metadata': data.get('extraction_info', {})}
            
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def call_openai_api(self, task: BulletPointTask) -> Optional[List[Dict]]:
        """Call OpenAI API to generate MCQ questions"""
        
        system_message = """You are an expert educational content creator specializing in creating high-quality multiple-choice questions for academic study materials. Your questions should test understanding, analysis, and application of knowledge."""
        
        user_prompt = f"""Context Information:
CHAPTER: {task.chapter_name}
SECTION: {task.section_name} (Section {task.section_number})
BULLET POINT: {task.bullet_point_text}

Create {task.questions_per_point} high-quality multiple-choice questions based on this bullet point.

Requirements:
- Each question should test understanding of specific facts/concepts from the bullet point
- 4 options per question (A, B, C, D)
- Only one correct answer per question
- Distractors should be plausible but clearly incorrect
- Include detailed explanations for ALL options (why correct option is right, why others are wrong)
- Questions should be academic-level and test comprehension, not just memorization
- Avoid questions that are too easy or too obvious
- Make questions that would be suitable for university-level study

Return ONLY a JSON structure with this exact format:
{{
  "questions": [
    {{
      "question": "question text here",
      "options": ["option A", "option B", "option C", "option D"],
      "correct": 0,
      "explanations": {{
        "0": "explanation for why option A is correct",
        "1": "explanation for why option B is incorrect",
        "2": "explanation for why option C is incorrect", 
        "3": "explanation for why option D is incorrect"
      }}
    }}
  ]
}}

Return ONLY the JSON, no other text:"""

        # Get next available client
        client, client_index = self.api_manager.get_next_client()
        
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            if response.choices and response.choices[0].message:
                content_response = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    # Clean the response (remove any markdown formatting)
                    if content_response.startswith('```json'):
                        content_response = content_response.replace('```json', '').replace('```', '').strip()
                    
                    questions_data = json.loads(content_response)
                    
                    # Validate structure
                    if 'questions' in questions_data and isinstance(questions_data['questions'], list):
                        questions = questions_data['questions']
                        
                        # Validate each question
                        valid_questions = []
                        for q in questions:
                            if (isinstance(q, dict) and 
                                'question' in q and 'options' in q and 'correct' in q and 'explanations' in q and
                                isinstance(q['options'], list) and len(q['options']) == 4 and
                                isinstance(q['correct'], int) and 0 <= q['correct'] <= 3 and
                                isinstance(q['explanations'], dict) and len(q['explanations']) == 4):
                                valid_questions.append(q)
                        
                        if valid_questions:
                            self.logger.debug(f"Generated {len(valid_questions)} valid questions using client {client_index + 1}")
                            return valid_questions
                    
                    self.logger.warning(f"Invalid question structure from API response")
                    return None
                    
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Failed to parse JSON response: {e}")
                    return None
            
        except Exception as e:
            self.logger.error(f"OpenAI API error with client {client_index + 1}: {e}")
            return None
    
    def process_bullet_point_task(self, task: BulletPointTask) -> Tuple[bool, Dict]:
        """Process a single bullet point task to generate questions"""
        self.logger.info(f"GENERATING MCQs: {task.section_name} - Bullet {task.bullet_point_index + 1}")
        
        # Call OpenAI API with retries
        questions = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                questions = self.call_openai_api(task)
                if questions:
                    break
                else:
                    self.logger.warning(f"Empty response from API, attempt {attempt + 1}/{max_retries}")
            except Exception as e:
                self.logger.warning(f"API call failed, attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        if not questions:
            self.logger.error(f"FAILED - Could not generate questions for bullet point: {task.bullet_point_text[:100]}...")
            return False, {}
        
        # Create result structure
        result = {
            'bullet_point_index': task.bullet_point_index,
            'bullet_point_text': task.bullet_point_text,
            'questions': questions,
            'generation_metadata': {
                'generated_timestamp': datetime.now().isoformat(),
                'openai_model': self.model_name,
                'questions_count': len(questions),
                'bullet_point_length': len(task.bullet_point_text)
            }
        }
        
        self.logger.info(f"SUCCESS: Generated {len(questions)} questions for bullet point {task.bullet_point_index + 1}")
        return True, result
    
    def process_file_parallel(self, file_path: Path) -> bool:
        """Process all bullet points in a file using parallel processing"""
        self.logger.info(f"PROCESSING FILE: {file_path.name}")
        
        # Load file
        file_data = self.load_extracted_file(file_path)
        if file_data is None:
            self.logger.error(f"Failed to load file: {file_path}")
            return False
        
        sections = file_data['sections']
        
        # Create tasks for all bullet points
        tasks = []
        section_data = {}
        
        for section_index, section in enumerate(sections):
            chapter_name = section.get('chapter_name', 'Unknown Chapter')
            section_name = section.get('section_name', 'Untitled Section')
            section_number = section.get('section_number', 'Unknown')
            bullet_points = section.get('openai_summarised_points', [])
            
            if not bullet_points:
                continue
            
            # Store section info
            section_data[section_index] = {
                'chapter_name': chapter_name,
                'section_name': section_name,
                'section_number': section_number,
                'source_file': section.get('source_file', file_path.name),
                'original_index': section.get('original_index', section_index),
                'total_bullet_points': len(bullet_points),
                'bullet_points': []
            }
            
            # Create tasks for each bullet point
            for bp_index, bullet_point in enumerate(bullet_points):
                if isinstance(bullet_point, str) and len(bullet_point.strip()) >= 20:
                    tasks.append(BulletPointTask(
                        file_path=file_path,
                        section_index=section_index,
                        bullet_point_index=bp_index,
                        chapter_name=chapter_name,
                        section_name=section_name,
                        section_number=section_number,
                        bullet_point_text=bullet_point,
                        questions_per_point=self.questions_per_point
                    ))
        
        if not tasks:
            self.logger.info("No valid bullet points found for question generation")
            self.processing_state.stats.skipped_files += 1
            return True
        
        self.logger.info(f"Generating questions for {len(tasks)} bullet points in parallel")
        
        # Process tasks in parallel
        processed_count = 0
        failed_count = 0
        total_questions = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {executor.submit(self.process_bullet_point_task, task): task for task in tasks}
            
            # Progress tracking
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    progress_task = progress.add_task(f"Generating MCQs for {file_path.name}", total=len(tasks))
                    
                    # Collect results as they complete
                    for future in concurrent.futures.as_completed(future_to_task):
                        task = future_to_task[future]
                        try:
                            success, result = future.result()
                            if success:
                                # Add result to section data
                                section_data[task.section_index]['bullet_points'].append(result)
                                processed_count += 1
                                total_questions += len(result['questions'])
                                self.processing_state.stats.completed_bullet_points += 1
                                self.processing_state.stats.total_questions_generated += len(result['questions'])
                            else:
                                failed_count += 1
                                self.processing_state.stats.failed_bullet_points += 1
                        except Exception as e:
                            self.logger.error(f"Task failed: {e}")
                            failed_count += 1
                            self.processing_state.stats.failed_bullet_points += 1
                        
                        progress.advance(progress_task)
                        
                        # Save progress periodically
                        if (processed_count + failed_count) % 5 == 0:
                            self.save_progress_file(file_path, section_data)
                            self.save_processing_state()
            else:
                # Fallback without rich
                for future in concurrent.futures.as_completed(future_to_task):
                    task = future_to_task[future]
                    try:
                        success, result = future.result()
                        if success:
                            section_data[task.section_index]['bullet_points'].append(result)
                            processed_count += 1
                            total_questions += len(result['questions'])
                            self.processing_state.stats.completed_bullet_points += 1
                            self.processing_state.stats.total_questions_generated += len(result['questions'])
                        else:
                            failed_count += 1
                            self.processing_state.stats.failed_bullet_points += 1
                    except Exception as e:
                        self.logger.error(f"Task failed: {e}")
                        failed_count += 1
                        self.processing_state.stats.failed_bullet_points += 1
                    
                    print(f"Completed: {processed_count + failed_count}/{len(tasks)}")
        
        # Final save
        self.save_final_file(file_path, section_data, file_data['metadata'])
        self.save_processing_state()
        
        self.logger.info(f"FILE COMPLETE: {file_path.name} - Generated {total_questions} questions from {processed_count} bullet points, Failed: {failed_count}")
        self.processing_state.stats.completed_files += 1
        
        return True
    
    def save_progress_file(self, file_path: Path, section_data: Dict):
        """Save progress file during processing"""
        try:
            output_file = self.output_dir / f"questions_{file_path.stem}.json"
            temp_file = output_file.with_suffix('.tmp')
            
            # Create temporary structure
            temp_data = {
                'generation_info': {
                    'source_file': file_path.name,
                    'generation_timestamp': datetime.now().isoformat(),
                    'status': 'in_progress',
                    'openai_model': self.model_name
                },
                'sections': list(section_data.values())
            }
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(temp_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Failed to save progress file: {e}")
    
    def save_final_file(self, file_path: Path, section_data: Dict, original_metadata: Dict):
        """Save final question file"""
        try:
            output_file = self.output_dir / f"questions_{file_path.stem}.json"
            
            # Calculate statistics
            total_sections = len(section_data)
            total_bullet_points = sum(len(s['bullet_points']) for s in section_data.values())
            total_questions = sum(len(bp['questions']) for s in section_data.values() for bp in s['bullet_points'])
            
            # Create final structure
            final_data = {
                'generation_info': {
                    'source_file': file_path.name,
                    'generation_timestamp': datetime.now().isoformat(),
                    'openai_model': self.model_name,
                    'questions_per_bullet_point': self.questions_per_point,
                    'total_sections': total_sections,
                    'total_bullet_points': total_bullet_points,
                    'total_questions_generated': total_questions,
                    'source_metadata': original_metadata
                },
                'sections': list(section_data.values())
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)
            
            # Remove temp file if exists
            temp_file = output_file.with_suffix('.tmp')
            if temp_file.exists():
                temp_file.unlink()
            
            self.logger.info(f"Saved {total_questions} questions to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save final file: {e}")
    
    def create_master_question_bank(self, processed_files: List[Path]):
        """Create master question bank with all questions"""
        self.logger.info("Creating master question bank...")
        
        all_sections = []
        total_questions = 0
        
        # Collect all sections from generated files
        for file_path in processed_files:
            question_file = self.output_dir / f"questions_{file_path.stem}.json"
            if question_file.exists():
                try:
                    with open(question_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    sections = data.get('sections', [])
                    all_sections.extend(sections)
                    
                    # Count questions
                    for section in sections:
                        for bp in section.get('bullet_points', []):
                            total_questions += len(bp.get('questions', []))
                    
                except Exception as e:
                    self.logger.error(f"Error reading question file {question_file}: {e}")
        
        if all_sections:
            master_data = {
                'master_question_bank_info': {
                    'creation_timestamp': datetime.now().isoformat(),
                    'total_sections': len(all_sections),
                    'total_questions': total_questions,
                    'source_folder': str(self.folder_path),
                    'openai_model': self.model_name,
                    'questions_per_bullet_point': self.questions_per_point
                },
                'sections': all_sections
            }
            
            master_file = self.output_dir / "master_question_bank.json"
            with open(master_file, 'w', encoding='utf-8') as f:
                json.dump(master_data, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✓ Master question bank created with {total_questions} questions: {master_file}[/green]")
    
    def run_generation(self) -> bool:
        """Main method to run the MCQ generation process"""
        self.logger.info("=== STARTING MULTI-API MCQ GENERATION PROCESS ===")
        self.logger.info(f"Input folder: {self.folder_path}")
        self.logger.info(f"Output folder: {self.output_dir}")
        self.logger.info(f"OpenAI model: {self.model_name}")
        self.logger.info(f"Questions per bullet point: {self.questions_per_point}")
        self.logger.info(f"API keys: {len(self.api_manager.api_keys)}")
        self.logger.info(f"Max workers: {self.max_workers}")
        
        # Discover files
        extracted_files = self.discover_extracted_files()
        if not extracted_files:
            self.logger.error("No extracted JSON files found to process")
            return False
        
        # Process files
        console.print(f"\n[bold]Processing {len(extracted_files)} files with {len(self.api_manager.api_keys)} API keys...[/bold]\n")
        
        processed_files = []
        for file_path in extracted_files:
            try:
                if self.process_file_parallel(file_path):
                    processed_files.append(file_path)
            except KeyboardInterrupt:
                self.logger.info("Process interrupted by user")
                self.save_processing_state()
                console.print("\n[yellow]Process interrupted. State saved. Resume with the same command.[/yellow]")
                return False
            except Exception as e:
                self.logger.error(f"Critical error processing {file_path}: {e}")
                continue
        
        # Create master question bank
        if processed_files:
            self.create_master_question_bank(processed_files)
        
        # Final statistics
        self.print_final_report()
        self.logger.info("=== MCQ GENERATION PROCESS COMPLETE ===")
        return True
    
    def print_final_report(self):
        """Print comprehensive final report"""
        stats = self.processing_state.stats
        duration = datetime.now() - datetime.fromisoformat(stats.start_time) if stats.start_time else None
        usage_stats = self.api_manager.get_usage_stats()
        
        console.print("\n" + "="*60)
        console.print("[bold]MCQ GENERATION COMPLETE - FINAL REPORT[/bold]")
        console.print("="*60)
        
        console.print(f"[bold]Files:[/bold]")
        console.print(f"  Total files: {stats.total_files}")
        console.print(f"  Completed files: {stats.completed_files}")
        console.print(f"  Skipped files: {stats.skipped_files}")
        
        console.print(f"\n[bold]Question Generation:[/bold]")
        console.print(f"  Total bullet points processed: {stats.completed_bullet_points}")
        console.print(f"  Bullet points failed: {stats.failed_bullet_points}")
        console.print(f"  Total questions generated: {stats.total_questions_generated}")
        console.print(f"  Average questions per bullet point: {stats.total_questions_generated / max(stats.completed_bullet_points, 1):.1f}")
        
        console.print(f"\n[bold]API Usage:[/bold]")
        console.print(f"  API keys used: {stats.api_keys_used}")
        for i, (key_partial, usage) in enumerate(usage_stats.items()):
            key_display = f"***{key_partial[-4:]}" if len(key_partial) > 4 else "***"
            console.print(f"  API Key {i+1} ({key_display}): {usage} requests")
        
        if duration:
            console.print(f"\n[bold]Performance:[/bold]")
            console.print(f"  Total duration: {duration}")
            if stats.completed_bullet_points > 0:
                rate = stats.completed_bullet_points / duration.total_seconds() * 60
                console.print(f"  Processing rate: {rate:.2f} bullet points/minute")
                q_rate = stats.total_questions_generated / duration.total_seconds() * 60
                console.print(f"  Question generation rate: {q_rate:.2f} questions/minute")
                console.print(f"  Parallel speedup: ~{len(self.api_manager.api_keys)}x faster")
        
        console.print(f"\n[bold]Output files saved to:[/bold] {self.output_dir}")
        console.print("="*60)

def main():
    """Main entry point"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Multi-API Wikipedia MCQ Question Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_mcq_questions.py /path/to/extracted/json/folder
  python generate_mcq_questions.py /path/to/extracted/json/folder --model gpt-3.5-turbo
  python generate_mcq_questions.py /path/to/extracted/json/folder --questions 3 --workers 8

Environment Variables:
  OPENAI_API_KEY      - Primary API key
  OPENAI_API_KEY_1    - Additional API key 1
  OPENAI_API_KEY_2    - Additional API key 2
  ... and so on

Output Structure:
  Each bullet point generates 2-3 MCQ questions with:
  - 4 multiple choice options
  - Correct answer index
  - Detailed explanations for all options
        """
    )
    
    parser.add_argument(
        'folder_path',
        help='Path to folder containing extracted Wikipedia JSON files'
    )
    
    parser.add_argument(
        '--model',
        default='gpt-4.1-mini',
        help='OpenAI model to use (default: gpt-4.1-mini)'
    )
    
    parser.add_argument(
        '--questions',
        type=int,
        default=2,
        choices=[1, 2, 3],
        help='Number of questions per bullet point (1-3, default: 2)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        help='Maximum number of parallel workers (default: API keys * 2)'
    )
    
    args = parser.parse_args()
    
    # Validate folder path
    folder_path = Path(args.folder_path)
    if not folder_path.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"❌ Error: Path is not a directory: {folder_path}")
        sys.exit(1)
    
    # Check for extracted files
    extracted_files = list(folder_path.glob("extracted_*.json"))
    flat_dataset = folder_path / "flat_dataset.json"
    
    if not extracted_files and not flat_dataset.exists():
        print(f"❌ Error: No extracted JSON files found in {folder_path}")
        print("Expected files: extracted_*.json or flat_dataset.json")
        sys.exit(1)
    
    # Initialize manager and run
    try:
        generator = MCQGenerator(
            folder_path=str(folder_path),
            model_name=args.model,
            questions_per_point=args.questions,
            max_workers=args.workers
        )
        
        success = generator.run_generation()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()