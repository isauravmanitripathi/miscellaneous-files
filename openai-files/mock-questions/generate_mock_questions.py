#!/usr/bin/env python3
"""
Enhanced Wikipedia MCQ Question Generator with Clean Output and Smart API Management
"""

import json
import os
import sys
import time
import logging
import random
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import argparse
from dataclasses import dataclass, asdict
from openai import OpenAI
from dotenv import load_dotenv
import threading

# Rich library for better console output (optional)
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
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
    """Enhanced statistics for tracking MCQ generation progress"""
    total_files: int = 0
    completed_files: int = 0
    total_bullet_points: int = 0
    completed_bullet_points: int = 0
    skipped_bullet_points: int = 0
    failed_bullet_points: int = 0
    total_questions_generated: int = 0
    start_time: Optional[str] = None
    api_keys_used: int = 0

@dataclass
class ProcessingState:
    """Enhanced state information for resume functionality"""
    folder_path: str
    completed_bullet_points: Dict[str, Dict[int, List[int]]] = None  # file -> section -> bullet_indices
    timestamp: Optional[str] = None
    stats: ProcessingStats = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = ProcessingStats()
        if self.completed_bullet_points is None:
            self.completed_bullet_points = {}

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
    task_id: str = ""

    def __post_init__(self):
        self.task_id = f"{self.file_path.stem}_{self.section_index}_{self.bullet_point_index}"

class EnhancedAPIKeyManager:
    """Enhanced API key manager with better load balancing and monitoring"""
    
    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.model_name = model_name
        self.api_keys = self.discover_api_keys()
        self.clients = self.initialize_clients()
        
        # Enhanced tracking
        self.usage_stats = {f"key_{i+1}": 0 for i in range(len(self.api_keys))}
        self.active_requests = {f"key_{i+1}": 0 for i in range(len(self.api_keys))}
        self.last_used = {f"key_{i+1}": 0 for i in range(len(self.api_keys))}
        self.errors = {f"key_{i+1}": 0 for i in range(len(self.api_keys))}
        
        self.lock = threading.Lock()
        self.current_index = 0
        
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
        
        return api_keys
    
    def initialize_clients(self) -> List[OpenAI]:
        """Initialize OpenAI clients for each API key"""
        clients = []
        for i, api_key in enumerate(self.api_keys):
            try:
                client = OpenAI(api_key=api_key)
                clients.append(client)
            except Exception as e:
                raise Exception(f"Failed to initialize API client {i+1}: {e}")
        return clients
    
    def get_next_client(self) -> Tuple[OpenAI, str, int]:
        """Get the next available client using intelligent load balancing"""
        with self.lock:
            # Find the key with least active requests and lowest usage
            best_key = None
            best_score = float('inf')
            
            for i, key_name in enumerate(self.usage_stats.keys()):
                # Score based on active requests (priority) and total usage
                score = (self.active_requests[key_name] * 100) + self.usage_stats[key_name]
                
                if score < best_score:
                    best_score = score
                    best_key = key_name
                    best_index = i
            
            # Update tracking
            self.usage_stats[best_key] += 1
            self.active_requests[best_key] += 1
            self.last_used[best_key] = time.time()
            
            return self.clients[best_index], best_key, best_index
    
    def release_client(self, key_name: str, success: bool = True):
        """Release a client after use"""
        with self.lock:
            if key_name in self.active_requests:
                self.active_requests[key_name] = max(0, self.active_requests[key_name] - 1)
                if not success:
                    self.errors[key_name] += 1
    
    def get_usage_summary(self) -> Dict:
        """Get comprehensive usage summary"""
        with self.lock:
            return {
                'total_keys': len(self.api_keys),
                'usage_stats': self.usage_stats.copy(),
                'active_requests': self.active_requests.copy(),
                'error_counts': self.errors.copy(),
                'total_requests': sum(self.usage_stats.values()),
                'total_errors': sum(self.errors.values())
            }

class CleanMCQGenerator:
    """
    Enhanced MCQ generator with clean output and smart API management
    """
    
    def __init__(self, folder_path: str, model_name: str = "gpt-4.1-mini", 
                 questions_per_point: int = 2, max_workers: int = None):
        self.folder_path = Path(folder_path)
        self.model_name = model_name
        self.questions_per_point = max(1, min(questions_per_point, 3))
        
        # Initialize enhanced API manager
        try:
            self.api_manager = EnhancedAPIKeyManager(model_name)
            self.max_workers = max_workers or min(len(self.api_manager.api_keys) * 2, 10)
        except Exception as e:
            console.print(f"[red]✗ API Initialization Failed: {e}[/red]")
            sys.exit(1)
        
        # Setup directories
        self.output_dir = self.folder_path.parent / "question_bank"
        self.logs_dir = self.output_dir / "logs"
        self.backups_dir = self.output_dir / "backups"
        
        for dir_path in [self.output_dir, self.logs_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Setup minimal logging (errors only to console)
        self.setup_minimal_logging()
        
        # Initialize state tracking
        self.state_file = self.logs_dir / "mcq_generation_state.json"
        self.processing_state = self.load_processing_state()
        self.processing_state.stats.api_keys_used = len(self.api_manager.api_keys)
        
        # Thread-safe data structures
        self.data_lock = threading.Lock()
        self.progress_counter = 0
        
        # Analyze existing progress
        self.analyze_existing_progress()
        
    def setup_minimal_logging(self):
        """Setup minimal logging - detailed logs to file, minimal to console"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        self.logger = logging.getLogger('MCQGenerator')
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(self.logs_dir / 'mcq_generation.log')
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        
        # Console handler only for errors
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('[ERROR] %(message)s'))
        console_handler.setLevel(logging.ERROR)
        self.logger.addHandler(console_handler)
    
    def load_processing_state(self) -> ProcessingState:
        """Load processing state from file or create new one"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                state = ProcessingState(
                    folder_path=data.get('folder_path', str(self.folder_path)),
                    completed_bullet_points=data.get('completed_bullet_points', {}),
                    timestamp=data.get('timestamp')
                )
                
                if 'stats' in data:
                    state.stats = ProcessingStats(**data['stats'])
                
                return state
            except Exception as e:
                self.logger.error(f"Failed to load processing state: {e}")
        
        # Create new state
        state = ProcessingState(folder_path=str(self.folder_path))
        state.stats.start_time = datetime.now().isoformat()
        return state
    
    def save_processing_state(self):
        """Save current processing state to file"""
        try:
            self.processing_state.timestamp = datetime.now().isoformat()
            
            state_dict = {
                'folder_path': self.processing_state.folder_path,
                'completed_bullet_points': self.processing_state.completed_bullet_points,
                'timestamp': self.processing_state.timestamp,
                'stats': asdict(self.processing_state.stats)
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_dict, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save processing state: {e}")
    
    def analyze_existing_progress(self):
        """Analyze existing question files to determine what's already been processed"""
        existing_files = list(self.output_dir.glob("questions_*.json"))
        
        total_existing_questions = 0
        total_existing_bullet_points = 0
        
        for question_file in existing_files:
            try:
                with open(question_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                source_file = data.get('generation_info', {}).get('source_file', '')
                if not source_file:
                    continue
                
                if source_file not in self.processing_state.completed_bullet_points:
                    self.processing_state.completed_bullet_points[source_file] = {}
                
                sections = data.get('sections', [])
                for section in sections:
                    section_index = section.get('original_index', 0)
                    
                    if section_index not in self.processing_state.completed_bullet_points[source_file]:
                        self.processing_state.completed_bullet_points[source_file][section_index] = []
                    
                    bullet_points = section.get('bullet_points', [])
                    for bp in bullet_points:
                        bp_index = bp.get('bullet_point_index', 0)
                        questions_count = len(bp.get('questions', []))
                        
                        if bp_index not in self.processing_state.completed_bullet_points[source_file][section_index]:
                            self.processing_state.completed_bullet_points[source_file][section_index].append(bp_index)
                            total_existing_bullet_points += 1
                            total_existing_questions += questions_count
                
            except Exception as e:
                self.logger.error(f"Failed to analyze existing file {question_file}: {e}")
        
        if total_existing_bullet_points > 0:
            self.processing_state.stats.completed_bullet_points = total_existing_bullet_points
            self.processing_state.stats.total_questions_generated = total_existing_questions
    
    def is_bullet_point_completed(self, file_name: str, section_index: int, bullet_point_index: int) -> bool:
        """Check if a specific bullet point has already been processed"""
        if file_name not in self.processing_state.completed_bullet_points:
            return False
        if section_index not in self.processing_state.completed_bullet_points[file_name]:
            return False
        return bullet_point_index in self.processing_state.completed_bullet_points[file_name][section_index]
    
    def mark_bullet_point_completed(self, file_name: str, section_index: int, bullet_point_index: int, questions_count: int):
        """Mark a bullet point as completed"""
        if file_name not in self.processing_state.completed_bullet_points:
            self.processing_state.completed_bullet_points[file_name] = {}
        if section_index not in self.processing_state.completed_bullet_points[file_name]:
            self.processing_state.completed_bullet_points[file_name][section_index] = []
        
        if bullet_point_index not in self.processing_state.completed_bullet_points[file_name][section_index]:
            self.processing_state.completed_bullet_points[file_name][section_index].append(bullet_point_index)
            self.processing_state.stats.completed_bullet_points += 1
            self.processing_state.stats.total_questions_generated += questions_count
    
    def discover_extracted_files(self) -> List[Path]:
        """Discover extracted JSON files in the input folder"""
        try:
            extracted_files = list(self.folder_path.glob("extracted_*.json"))
            if not extracted_files:
                flat_dataset = self.folder_path / "flat_dataset.json"
                if flat_dataset.exists():
                    extracted_files = [flat_dataset]
            
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
            
            if 'sections' in data:
                sections = data['sections']
            elif isinstance(data, list):
                sections = data
            else:
                return None
            
            return {'sections': sections, 'metadata': data.get('extraction_info', {})}
            
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def randomize_question_options(self, question_data: Dict) -> Dict:
        """Randomly shuffle options and update correct index and explanations"""
        try:
            options = question_data['options'].copy()
            explanations = question_data['explanations'].copy()
            correct_index = question_data['correct']
            
            # Create shuffled indices
            indices = list(range(4))
            random.shuffle(indices)
            
            # Rearrange options and explanations
            new_options = [options[i] for i in indices]
            new_explanations = {}
            for new_pos, old_pos in enumerate(indices):
                new_explanations[str(new_pos)] = explanations[str(old_pos)]
            
            # Find new position of correct answer
            new_correct_index = indices.index(correct_index)
            
            return {
                'question': question_data['question'],
                'options': new_options,
                'correct': new_correct_index,
                'explanations': new_explanations
            }
            
        except Exception as e:
            return question_data
    
    def call_openai_api(self, task: BulletPointTask) -> Tuple[Optional[List[Dict]], str]:
        """Call OpenAI API to generate MCQ questions - returns questions and API key used"""
        
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
        client, key_name, key_index = self.api_manager.get_next_client()
        
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
                    if content_response.startswith('```json'):
                        content_response = content_response.replace('```json', '').replace('```', '').strip()
                    
                    questions_data = json.loads(content_response)
                    
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
                            self.api_manager.release_client(key_name, success=True)
                            return valid_questions, key_name
                    
                    self.api_manager.release_client(key_name, success=False)
                    return None, key_name
                    
                except json.JSONDecodeError:
                    self.api_manager.release_client(key_name, success=False)
                    return None, key_name
            
        except Exception as e:
            self.api_manager.release_client(key_name, success=False)
            self.logger.error(f"OpenAI API error with {key_name}: {e}")
            return None, key_name
    
    def process_bullet_point_task(self, task: BulletPointTask) -> Tuple[bool, Dict, str]:
        """Process a single bullet point task to generate questions"""
        
        # Check if already completed
        if self.is_bullet_point_completed(task.file_path.name, task.section_index, task.bullet_point_index):
            self.processing_state.stats.skipped_bullet_points += 1
            return True, {'skipped': True}, "cached"
        
        # Call OpenAI API with retries
        questions = None
        api_key_used = "none"
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                questions, api_key_used = self.call_openai_api(task)
                if questions:
                    break
                else:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        if not questions:
            self.processing_state.stats.failed_bullet_points += 1
            return False, {}, api_key_used
        
        # Randomize each question's options
        randomized_questions = []
        for question in questions:
            randomized_question = self.randomize_question_options(question)
            randomized_questions.append(randomized_question)
        
        # Create result structure
        result = {
            'bullet_point_index': task.bullet_point_index,
            'bullet_point_text': task.bullet_point_text,
            'questions': randomized_questions,
            'generation_metadata': {
                'generated_timestamp': datetime.now().isoformat(),
                'openai_model': self.model_name,
                'questions_count': len(randomized_questions),
                'bullet_point_length': len(task.bullet_point_text),
                'options_randomized': True,
                'api_key_used': api_key_used,
                'task_id': task.task_id
            }
        }
        
        # Mark as completed
        self.mark_bullet_point_completed(task.file_path.name, task.section_index, task.bullet_point_index, len(randomized_questions))
        
        return True, result, api_key_used
    
    def create_clean_progress_display(self, current: int, total: int, chapter: str, section: str, api_key: str, status: str):
        """Create clean, minimal progress display"""
        progress_pct = (current / total * 100) if total > 0 else 0
        
        # Truncate long names
        chapter_short = chapter[:20] + "..." if len(chapter) > 23 else chapter
        section_short = section[:25] + "..." if len(section) > 28 else section
        
        if RICH_AVAILABLE:
            status_color = {
                'success': 'green',
                'failed': 'red',
                'skipped': 'yellow',
                'processing': 'blue'
            }.get(status, 'white')
            
            console.print(f"[{status_color}]{status.upper():<9}[/{status_color}] "
                         f"[cyan]{current:3d}/{total:<3d}[/cyan] "
                         f"[magenta]{progress_pct:5.1f}%[/magenta] "
                         f"[blue]{chapter_short:<23}[/blue] "
                         f"[green]{section_short:<28}[/green] "
                         f"[yellow]{api_key}[/yellow]")
        else:
            print(f"{status.upper():<9} {current:3d}/{total:<3d} {progress_pct:5.1f}% "
                  f"{chapter_short:<23} {section_short:<28} {api_key}")
    
    def process_file_parallel(self, file_path: Path) -> bool:
        """Process all bullet points in a file using parallel processing"""
        
        # Load file
        file_data = self.load_extracted_file(file_path)
        if file_data is None:
            return False
        
        sections = file_data['sections']
        
        # Create tasks for unprocessed bullet points only
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
            
            # Create tasks for unprocessed bullet points only
            for bp_index, bullet_point in enumerate(bullet_points):
                if (isinstance(bullet_point, str) and len(bullet_point.strip()) >= 20 and
                    not self.is_bullet_point_completed(file_path.name, section_index, bp_index)):
                    
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
            self.processing_state.stats.completed_files += 1
            return True
        
        # Show file processing header
        if RICH_AVAILABLE:
            console.print(f"\n[bold blue]Processing: {file_path.name}[/bold blue]")
            console.print(f"[cyan]Found {len(tasks)} unprocessed bullet points[/cyan]")
            console.print("-" * 100)
            console.print(f"{'STATUS':<9} {'PROGRESS':<7} {'%':<6} {'CHAPTER':<23} {'SECTION':<28} {'API'}")
            console.print("-" * 100)
        else:
            print(f"\nProcessing: {file_path.name}")
            print(f"Found {len(tasks)} unprocessed bullet points")
            print("-" * 100)
            print(f"{'STATUS':<9} {'PROGRESS':<7} {'%':<6} {'CHAPTER':<23} {'SECTION':<28} {'API'}")
            print("-" * 100)
        
        # Process tasks in parallel
        processed_count = 0
        total_tasks = len(tasks)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {executor.submit(self.process_bullet_point_task, task): task for task in tasks}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    success, result, api_key = future.result()
                    processed_count += 1
                    
                    if success and not result.get('skipped', False):
                        # Add result to section data
                        section_data[task.section_index]['bullet_points'].append(result)
                        self.create_clean_progress_display(
                            processed_count, total_tasks,
                            task.chapter_name, task.section_name,
                            api_key, 'success'
                        )
                    elif result.get('skipped', False):
                        self.create_clean_progress_display(
                            processed_count, total_tasks,
                            task.chapter_name, task.section_name,
                            'cached', 'skipped'
                        )
                    else:
                        self.create_clean_progress_display(
                            processed_count, total_tasks,
                            task.chapter_name, task.section_name,
                            api_key, 'failed'
                        )
                        
                except Exception as e:
                    processed_count += 1
                    self.create_clean_progress_display(
                        processed_count, total_tasks,
                        task.chapter_name, task.section_name,
                        'error', 'failed'
                    )
                    self.logger.error(f"Task failed: {e}")
                
                # Save progress periodically
                if processed_count % 10 == 0:
                    self.save_updated_file(file_path, section_data, file_data['metadata'])
                    self.save_processing_state()
        
        # Final save
        self.save_updated_file(file_path, section_data, file_data['metadata'])
        self.save_processing_state()
        
        self.processing_state.stats.completed_files += 1
        return True
    
    def save_updated_file(self, file_path: Path, section_data: Dict, original_metadata: Dict):
        """Save or update the question file with new results"""
        try:
            output_file = self.output_dir / f"questions_{file_path.stem}.json"
            
            # Load existing data if file exists
            existing_data = {}
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Merge or create sections
            all_sections = existing_data.get('sections', [])
            
            # Update with new data
            for section_index, new_section in section_data.items():
                # Find existing section or add new one
                existing_section_index = None
                for i, section in enumerate(all_sections):
                    if (section.get('original_index') == new_section.get('original_index') and
                        section.get('source_file') == new_section.get('source_file')):
                        existing_section_index = i
                        break
                
                if existing_section_index is not None:
                    # Merge bullet points
                    existing_bullets = all_sections[existing_section_index].get('bullet_points', [])
                    new_bullets = new_section.get('bullet_points', [])
                    
                    # Add only new bullet points
                    for new_bp in new_bullets:
                        bp_index = new_bp.get('bullet_point_index')
                        # Check if already exists
                        exists = any(bp.get('bullet_point_index') == bp_index for bp in existing_bullets)
                        if not exists:
                            existing_bullets.append(new_bp)
                    
                    all_sections[existing_section_index]['bullet_points'] = existing_bullets
                    all_sections[existing_section_index]['total_bullet_points'] = len(existing_bullets)
                else:
                    # Add new section
                    all_sections.append(new_section)
            
            # Calculate statistics
            total_sections = len(all_sections)
            total_bullet_points = sum(len(s.get('bullet_points', [])) for s in all_sections)
            total_questions = sum(len(bp.get('questions', [])) for s in all_sections for bp in s.get('bullet_points', []))
            
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
                'sections': all_sections
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Failed to save updated file: {e}")
    
    def create_master_question_bank(self, processed_files: List[Path]):
        """Create master question bank with all questions"""
        all_sections = []
        total_questions = 0
        
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
    
    def show_api_usage_summary(self):
        """Display clean API usage summary"""
        usage_summary = self.api_manager.get_usage_summary()
        
        if RICH_AVAILABLE:
            console.print("\n" + "="*80)
            console.print("[bold]API Usage Summary[/bold]")
            console.print("="*80)
            
            table = Table()
            table.add_column("API Key", style="cyan")
            table.add_column("Requests", style="green", justify="right")
            table.add_column("Errors", style="red", justify="right")
            table.add_column("Success Rate", style="yellow", justify="right")
            
            for i, (key_name, requests) in enumerate(usage_summary['usage_stats'].items()):
                errors = usage_summary['error_counts'][key_name]
                success_rate = ((requests - errors) / requests * 100) if requests > 0 else 0
                
                table.add_row(
                    key_name,
                    str(requests),
                    str(errors),
                    f"{success_rate:.1f}%"
                )
            
            console.print(table)
            console.print(f"[bold]Total Requests:[/bold] {usage_summary['total_requests']}")
            console.print(f"[bold]Total Errors:[/bold] {usage_summary['total_errors']}")
            console.print("="*80)
        else:
            print("\n" + "="*80)
            print("API Usage Summary")
            print("="*80)
            for key_name, requests in usage_summary['usage_stats'].items():
                errors = usage_summary['error_counts'][key_name]
                success_rate = ((requests - errors) / requests * 100) if requests > 0 else 0
                print(f"{key_name}: {requests} requests, {errors} errors, {success_rate:.1f}% success")
            print(f"Total Requests: {usage_summary['total_requests']}")
            print(f"Total Errors: {usage_summary['total_errors']}")
            print("="*80)
    
    def run_generation(self) -> bool:
        """Main method to run the MCQ generation process"""
        
        # Show startup info
        if RICH_AVAILABLE:
            startup_panel = Panel.fit(
                f"[bold]MCQ Generator Started[/bold]\n"
                f"Model: [cyan]{self.model_name}[/cyan]\n"
                f"API Keys: [green]{len(self.api_manager.api_keys)}[/green]\n"
                f"Workers: [yellow]{self.max_workers}[/yellow]\n"
                f"Questions per bullet: [magenta]{self.questions_per_point}[/magenta]",
                title="Configuration",
                border_style="blue"
            )
            console.print(startup_panel)
        else:
            print("="*60)
            print("MCQ Generator Started")
            print(f"Model: {self.model_name}")
            print(f"API Keys: {len(self.api_manager.api_keys)}")
            print(f"Workers: {self.max_workers}")
            print(f"Questions per bullet: {self.questions_per_point}")
            print("="*60)
        
        # Discover files
        extracted_files = self.discover_extracted_files()
        if not extracted_files:
            if RICH_AVAILABLE:
                console.print("[red]✗ No extracted JSON files found to process[/red]")
            else:
                print("✗ No extracted JSON files found to process")
            return False
        
        # Show existing progress
        if self.processing_state.stats.completed_bullet_points > 0:
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Resuming: {self.processing_state.stats.completed_bullet_points} bullet points already completed[/green]")
            else:
                print(f"✓ Resuming: {self.processing_state.stats.completed_bullet_points} bullet points already completed")
        
        # Process files
        processed_files = []
        for file_path in extracted_files:
            try:
                if self.process_file_parallel(file_path):
                    processed_files.append(file_path)
            except KeyboardInterrupt:
                if RICH_AVAILABLE:
                    console.print("\n[yellow]⚠ Process interrupted. Progress saved.[/yellow]")
                else:
                    print("\n⚠ Process interrupted. Progress saved.")
                self.save_processing_state()
                return False
            except Exception as e:
                self.logger.error(f"Critical error processing {file_path}: {e}")
                continue
        
        # Create master question bank
        if processed_files:
            if RICH_AVAILABLE:
                console.print("\n[blue]Creating master question bank...[/blue]")
            else:
                print("\nCreating master question bank...")
            self.create_master_question_bank(processed_files)
        
        # Show final summary
        self.show_api_usage_summary()
        self.print_final_summary()
        
        return True
    
    def print_final_summary(self):
        """Print comprehensive final summary"""
        stats = self.processing_state.stats
        
        if RICH_AVAILABLE:
            summary_panel = Panel.fit(
                f"[bold green]✓ Processing Complete[/bold green]\n\n"
                f"[bold]Files Processed:[/bold] {stats.completed_files}\n"
                f"[bold]Bullet Points:[/bold] {stats.completed_bullet_points} completed, {stats.skipped_bullet_points} skipped, {stats.failed_bullet_points} failed\n"
                f"[bold]Questions Generated:[/bold] {stats.total_questions_generated}\n"
                f"[bold]Average per Bullet:[/bold] {stats.total_questions_generated / max(stats.completed_bullet_points, 1):.1f}\n\n"
                f"[bold]Output Location:[/bold] {self.output_dir}",
                title="Final Summary",
                border_style="green"
            )
            console.print(summary_panel)
        else:
            print("\n" + "="*60)
            print("✓ Processing Complete")
            print("="*60)
            print(f"Files Processed: {stats.completed_files}")
            print(f"Bullet Points: {stats.completed_bullet_points} completed, {stats.skipped_bullet_points} skipped, {stats.failed_bullet_points} failed")
            print(f"Questions Generated: {stats.total_questions_generated}")
            print(f"Average per Bullet: {stats.total_questions_generated / max(stats.completed_bullet_points, 1):.1f}")
            print(f"Output Location: {self.output_dir}")
            print("="*60)

def main():
    """Main entry point"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Enhanced Wikipedia MCQ Question Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('folder_path', help='Path to folder containing extracted Wikipedia JSON files')
    parser.add_argument('--model', default='gpt-4.1-mini', help='OpenAI model to use (default: gpt-4.1-mini)')
    parser.add_argument('--questions', type=int, default=2, choices=[1, 2, 3], help='Number of questions per bullet point (1-3, default: 2)')
    parser.add_argument('--workers', type=int, help='Maximum number of parallel workers (default: API keys * 2)')
    
    args = parser.parse_args()
    
    # Validate folder path
    folder_path = Path(args.folder_path)
    if not folder_path.exists():
        console.print(f"[red]❌ Error: Folder not found: {folder_path}[/red]")
        sys.exit(1)
    
    if not folder_path.is_dir():
        console.print(f"[red]❌ Error: Path is not a directory: {folder_path}[/red]")
        sys.exit(1)
    
    # Check for extracted files
    extracted_files = list(folder_path.glob("extracted_*.json"))
    flat_dataset = folder_path / "flat_dataset.json"
    
    if not extracted_files and not flat_dataset.exists():
        console.print(f"[red]❌ Error: No extracted JSON files found in {folder_path}[/red]")
        console.print("[yellow]Expected files: extracted_*.json or flat_dataset.json[/yellow]")
        sys.exit(1)
    
    # Initialize generator and run
    try:
        generator = CleanMCQGenerator(
            folder_path=str(folder_path),
            model_name=args.model,
            questions_per_point=args.questions,
            max_workers=args.workers
        )
        
        success = generator.run_generation()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Process interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Critical error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()