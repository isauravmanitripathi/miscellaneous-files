#!/usr/bin/env python3
"""
Cluster-Based Wikipedia MCQ Question Generator
Processes bullet points in clusters of 2-3 for efficiency, generating 4 questions per cluster
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
class SectionCompletion:
    """Track completion status of a specific chapter-section"""
    chapter_name: str
    section_number: str
    section_name: str
    total_bullets: int
    completed_bullets: List[int]
    missing_bullets: List[int]
    completion_percentage: float

    def is_complete(self) -> bool:
        return len(self.missing_bullets) == 0

@dataclass
class ProcessingStats:
    """Enhanced statistics for tracking MCQ generation progress"""
    total_files: int = 0
    completed_files: int = 0
    total_sections: int = 0
    completed_sections: int = 0
    total_bullet_points: int = 0
    completed_bullet_points: int = 0
    remaining_bullet_points: int = 0
    failed_bullet_points: int = 0
    total_clusters_processed: int = 0
    total_questions_generated: int = 0
    start_time: Optional[str] = None
    api_keys_used: int = 0

@dataclass
class BulletPointClusterTask:
    """Represents a cluster of bullet points to process together"""
    file_path: Path
    chapter_name: str
    section_number: str
    section_name: str
    section_index: int
    bullet_point_cluster: List[Tuple[int, str]]  # [(index, text), (index, text), ...]
    cluster_id: str = ""

    def __post_init__(self):
        indices = [str(bp[0]) for bp in self.bullet_point_cluster]
        self.cluster_id = f"{self.chapter_name}_{self.section_number}_cluster_{'_'.join(indices)}"

    @property
    def cluster_size(self) -> int:
        return len(self.bullet_point_cluster)

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

class ClusterMCQGenerator:
    """
    Cluster-based MCQ generator that processes bullet points in batches
    """
    
    def __init__(self, folder_path: str, model_name: str = "gpt-4.1-mini", 
                 cluster_size: int = 3, max_workers: int = None):
        self.folder_path = Path(folder_path)
        self.model_name = model_name
        self.cluster_size = max(2, min(cluster_size, 3))  # Limit 2-3
        
        # Initialize enhanced API manager
        try:
            self.api_manager = EnhancedAPIKeyManager(model_name)
            self.max_workers = max_workers or min(len(self.api_manager.api_keys) * 2, 8)
        except Exception as e:
            console.print(f"[red]✗ API Initialization Failed: {e}[/red]")
            sys.exit(1)
        
        # Setup directories
        self.output_dir = self.folder_path.parent / "question_bank"
        self.logs_dir = self.output_dir / "logs"
        self.backups_dir = self.output_dir / "backups"
        
        for dir_path in [self.output_dir, self.logs_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Setup minimal logging
        self.setup_minimal_logging()
        
        # Initialize statistics
        self.stats = ProcessingStats()
        self.stats.api_keys_used = len(self.api_manager.api_keys)
        self.stats.start_time = datetime.now().isoformat()
        
        # Thread-safe data structures
        self.data_lock = threading.Lock()
        
    def setup_minimal_logging(self):
        """Setup minimal logging - detailed logs to file, minimal to console"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        self.logger = logging.getLogger('ClusterMCQGenerator')
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(self.logs_dir / 'cluster_mcq_generation.log')
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        
        # Console handler only for errors
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('[ERROR] %(message)s'))
        console_handler.setLevel(logging.ERROR)
        self.logger.addHandler(console_handler)
    
    def validate_questions(self, questions: List[Dict]) -> bool:
        """Validate that questions are complete and properly formatted"""
        if not questions or len(questions) == 0:
            return False
        
        for question in questions:
            # Check required fields exist
            required_fields = ['question', 'options', 'correct', 'explanations']
            if not all(field in question for field in required_fields):
                return False
            
            # Check options count
            if not isinstance(question['options'], list) or len(question['options']) != 4:
                return False
            
            # Check correct index is valid
            if not isinstance(question['correct'], int) or not (0 <= question['correct'] <= 3):
                return False
            
            # Check explanations exist for all options
            if not isinstance(question['explanations'], dict) or len(question['explanations']) != 4:
                return False
            
            # Check no empty strings
            if not question['question'].strip():
                return False
            
            if any(not str(opt).strip() for opt in question['options']):
                return False
            
            # Check all explanation keys exist
            if not all(str(i) in question['explanations'] for i in range(4)):
                return False
        
        return True
    
    def create_bullet_point_clusters(self, missing_bullets: List[int], bullet_points: List[str]) -> List[List[Tuple[int, str]]]:
        """
        Group missing bullet points into clusters of 2-3
        Returns clusters with (index, content) tuples
        """
        clusters = []
        
        for i in range(0, len(missing_bullets), self.cluster_size):
            cluster_indices = missing_bullets[i:i + self.cluster_size]
            cluster_content = []
            
            for idx in cluster_indices:
                if idx < len(bullet_points) and isinstance(bullet_points[idx], str):
                    bullet_text = bullet_points[idx].strip()
                    if len(bullet_text) >= 20:  # Only include substantial bullet points
                        cluster_content.append((idx, bullet_text))
            
            if cluster_content:  # Only add non-empty clusters
                clusters.append(cluster_content)
        
        return clusters
    
    def analyze_section_completion(self, original_file_data: Dict, question_file_path: Path) -> Dict[str, SectionCompletion]:
        """
        Analyze completion status for each chapter-section combination
        Returns a map of section_key -> SectionCompletion
        """
        completion_map = {}
        
        # Scan original file to establish baseline
        sections = original_file_data.get('sections', [])
        if isinstance(original_file_data, list):
            sections = original_file_data
        
        for section_index, section in enumerate(sections):
            chapter_name = section.get('chapter_name', 'Unknown Chapter')
            section_number = section.get('section_number', f'section_{section_index}')
            section_name = section.get('section_name', 'Untitled Section')
            bullet_points = section.get('openai_summarised_points', [])
            
            # Create unique key for this chapter-section
            section_key = f"{chapter_name}_{section_number}"
            total_bullets = len(bullet_points)
            
            completion_map[section_key] = SectionCompletion(
                chapter_name=chapter_name,
                section_number=section_number,
                section_name=section_name,
                total_bullets=total_bullets,
                completed_bullets=[],
                missing_bullets=list(range(total_bullets)),
                completion_percentage=0.0
            )
        
        # Scan existing question file (if exists)
        if question_file_path.exists():
            try:
                with open(question_file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                existing_sections = existing_data.get('sections', [])
                for section in existing_sections:
                    chapter_name = section.get('chapter_name', 'Unknown Chapter')
                    section_number = section.get('section_number', 'unknown')
                    section_key = f"{chapter_name}_{section_number}"
                    
                    if section_key in completion_map:
                        # Check which bullet points have valid questions
                        bullet_points = section.get('bullet_points', [])
                        for bp in bullet_points:
                            bp_index = bp.get('bullet_point_index', -1)
                            questions = bp.get('questions', [])
                            
                            # Validate questions are complete and valid
                            if bp_index >= 0 and self.validate_questions(questions):
                                if bp_index in completion_map[section_key].missing_bullets:
                                    completion_map[section_key].completed_bullets.append(bp_index)
                                    completion_map[section_key].missing_bullets.remove(bp_index)
                        
                        # Update completion percentage
                        total = completion_map[section_key].total_bullets
                        completed = len(completion_map[section_key].completed_bullets)
                        completion_map[section_key].completion_percentage = (completed / total * 100) if total > 0 else 0
                
            except Exception as e:
                self.logger.error(f"Failed to analyze existing question file {question_file_path}: {e}")
        
        return completion_map
    
    def show_resume_info(self, completion_maps: Dict[str, Dict[str, SectionCompletion]]):
        """Show clear resume information across all files"""
        total_sections = 0
        completed_sections = 0
        total_bullets = 0
        completed_bullets = 0
        
        for file_name, completion_map in completion_maps.items():
            for section_completion in completion_map.values():
                total_sections += 1
                total_bullets += section_completion.total_bullets
                completed_bullets += len(section_completion.completed_bullets)
                
                if section_completion.is_complete():
                    completed_sections += 1
        
        remaining_bullets = total_bullets - completed_bullets
        estimated_clusters = (remaining_bullets + self.cluster_size - 1) // self.cluster_size  # Ceiling division
        
        # Update global stats
        self.stats.total_sections = total_sections
        self.stats.completed_sections = completed_sections
        self.stats.total_bullet_points = total_bullets
        self.stats.completed_bullet_points = completed_bullets
        self.stats.remaining_bullet_points = remaining_bullets
        
        if total_bullets > 0:
            if RICH_AVAILABLE:
                resume_panel = Panel.fit(
                    f"[bold]Cluster Resume Analysis[/bold]\n\n"
                    f"[green]Sections:[/green] {completed_sections}/{total_sections} complete\n"
                    f"[green]Bullet Points:[/green] {completed_bullets}/{total_bullets} complete\n"
                    f"[yellow]Remaining:[/yellow] {remaining_bullets} bullet points\n"
                    f"[cyan]Estimated Clusters:[/cyan] {estimated_clusters} clusters to process\n"
                    f"[magenta]Cluster Size:[/magenta] {self.cluster_size} bullet points per cluster\n"
                    f"[blue]Questions per Cluster:[/blue] 4 questions\n"
                    f"[cyan]Overall Progress:[/cyan] {completed_bullets/total_bullets*100:.1f}%",
                    title="Resume Status",
                    border_style="green" if remaining_bullets == 0 else "yellow"
                )
                console.print(resume_panel)
            else:
                print("="*70)
                print("Cluster Resume Analysis")
                print("="*70)
                print(f"Sections: {completed_sections}/{total_sections} complete")
                print(f"Bullet Points: {completed_bullets}/{total_bullets} complete")
                print(f"Remaining: {remaining_bullets} bullet points")
                print(f"Estimated Clusters: {estimated_clusters} clusters to process")
                print(f"Cluster Size: {self.cluster_size} bullet points per cluster")
                print(f"Questions per Cluster: 4 questions")
                print(f"Overall Progress: {completed_bullets/total_bullets*100:.1f}%")
                print("="*70)
    
    def create_cluster_tasks_from_completion_map(self, file_path: Path, original_data: Dict, completion_map: Dict[str, SectionCompletion]) -> List[BulletPointClusterTask]:
        """Create cluster tasks ONLY for missing bullet points"""
        tasks = []
        
        sections = original_data.get('sections', [])
        if isinstance(original_data, list):
            sections = original_data
        
        for section_index, section in enumerate(sections):
            chapter_name = section.get('chapter_name', 'Unknown Chapter')
            section_number = section.get('section_number', f'section_{section_index}')
            section_name = section.get('section_name', 'Untitled Section')
            section_key = f"{chapter_name}_{section_number}"
            
            if section_key in completion_map:
                missing_bullets = completion_map[section_key].missing_bullets
                bullet_points = section.get('openai_summarised_points', [])
                
                if missing_bullets:
                    # Create clusters from missing bullet points
                    clusters = self.create_bullet_point_clusters(missing_bullets, bullet_points)
                    
                    for cluster in clusters:
                        if cluster:  # Only create task if cluster has content
                            tasks.append(BulletPointClusterTask(
                                file_path=file_path,
                                chapter_name=chapter_name,
                                section_number=section_number,
                                section_name=section_name,
                                section_index=section_index,
                                bullet_point_cluster=cluster
                            ))
        
        return tasks
    
    def discover_extracted_files(self) -> List[Path]:
        """Discover extracted JSON files in the input folder"""
        try:
            extracted_files = list(self.folder_path.glob("extracted_*.json"))
            if not extracted_files:
                flat_dataset = self.folder_path / "flat_dataset.json"
                if flat_dataset.exists():
                    extracted_files = [flat_dataset]
            
            self.stats.total_files = len(extracted_files)
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
    
    def format_bullet_cluster(self, cluster: List[Tuple[int, str]]) -> str:
        """Format bullet point cluster for the API prompt"""
        formatted_points = []
        for i, (bp_index, bp_text) in enumerate(cluster, 1):
            formatted_points.append(f"BULLET POINT {i} (Index {bp_index}): {bp_text}")
        
        return "\n\n".join(formatted_points)
    
    def call_openai_api(self, task: BulletPointClusterTask) -> Tuple[Optional[List[Dict]], str]:
        """Call OpenAI API to generate UPSC-style MCQ questions for a cluster"""
        
        system_message = """You are an expert question setter for UPSC Civil Services Examination and other prestigious government competitive exams in India. You specialize in creating analytical, application-based multiple-choice questions that test deep understanding and critical thinking across related topics."""
        
        cluster_size = len(task.bullet_point_cluster)
        
        user_prompt = f"""Context Information:
CHAPTER: {task.chapter_name}
SECTION: {task.section_name} (Section {task.section_number})

BULLET POINTS CLUSTER:
{self.format_bullet_cluster(task.bullet_point_cluster)}

Create exactly 4 high-quality UPSC-style multiple-choice questions based on the {cluster_size} bullet points above.

CRITICAL REQUIREMENTS:

1. CLUSTER PROCESSING:
   - Generate exactly 4 questions total for the entire cluster
   - Draw insights from ALL bullet points in the cluster
   - Create questions that synthesize information across bullet points
   - Ensure questions complement each other and cover different aspects

2. QUESTION DISTRIBUTION:
   - Questions should cover the breadth of topics in the cluster
   - Each question can focus on one bullet point OR combine multiple bullet points
   - Prioritize analytical and application-based questions over factual recall

3. UPSC EXAMINATION PATTERN:
   - Use phrases like: "Which of the following statements is/are correct?", "The most appropriate explanation...", "In the context of...", "Consider the following statements..."
   - Test analytical ability, logical reasoning, and application of concepts
   - Create scenario-based questions requiring synthesis of the knowledge
   - Avoid direct factual recall questions

4. QUESTION TYPES (vary across the 4 questions):
   - Analytical reasoning and cause-effect relationships
   - Application scenarios and policy implications  
   - Comparative analysis across the bullet points
   - Conceptual understanding and synthesis

5. OPTION QUALITY:
   - All 4 options must be plausible and well-researched
   - Distractors based on common misconceptions or closely related concepts
   - Options should require careful analysis to distinguish correct from incorrect
   - Avoid obviously wrong options

6. EXPLANATION QUALITY:
   - Comprehensive explanations for ALL options
   - Connect explanations back to the original bullet points
   - Include additional context that enhances learning
   - Reference specific bullet points when relevant

EXAMPLE APPROACH:
- Question 1: Focus primarily on bullet point 1 concepts
- Question 2: Combine insights from bullet points 1 and 2
- Question 3: Analyze bullet point 2 in broader context
- Question 4: Synthesize all bullet points or focus on bullet point 3

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
      }},
      "source_bullet_points": [0, 1]
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
                max_tokens=4000  # Increased for cluster processing
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
                        
                        # Validate each question and ensure we have exactly 4
                        valid_questions = []
                        for q in questions[:4]:  # Take only first 4 questions
                            if (isinstance(q, dict) and 
                                'question' in q and 'options' in q and 'correct' in q and 'explanations' in q and
                                isinstance(q['options'], list) and len(q['options']) == 4 and
                                isinstance(q['correct'], int) and 0 <= q['correct'] <= 3 and
                                isinstance(q['explanations'], dict) and len(q['explanations']) == 4):
                                valid_questions.append(q)
                        
                        if len(valid_questions) == 4:  # Must have exactly 4 valid questions
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
    
    def process_cluster_task(self, task: BulletPointClusterTask) -> Tuple[bool, List[Dict], str]:
        """Process a cluster task to generate 4 questions for the cluster"""
        
        # Call OpenAI API with retries
        questions = None
        api_key_used = "none"
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                questions, api_key_used = self.call_openai_api(task)
                if questions and len(questions) == 4:
                    break
                else:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        if not questions or len(questions) != 4:
            self.stats.failed_bullet_points += len(task.bullet_point_cluster)
            return False, [], api_key_used
        
        # Randomize each question's options
        randomized_questions = []
        for question in questions:
            randomized_question = self.randomize_question_options(question)
            randomized_questions.append(randomized_question)
        
        # Create results for each bullet point in the cluster
        cluster_results = []
        questions_per_bullet = 4 / len(task.bullet_point_cluster)  # Distribute questions
        
        # Assign questions to bullet points (simple distribution)
        question_index = 0
        for i, (bp_index, bp_text) in enumerate(task.bullet_point_cluster):
            # Calculate how many questions this bullet point should get
            if i == len(task.bullet_point_cluster) - 1:
                # Last bullet point gets remaining questions
                bullet_questions = randomized_questions[question_index:]
            else:
                # Other bullet points get proportional share
                num_questions = max(1, int(questions_per_bullet * (i + 1)) - question_index)
                bullet_questions = randomized_questions[question_index:question_index + num_questions]
                question_index += num_questions
            
            if bullet_questions:  # Only create result if there are questions
                result = {
                    'bullet_point_index': bp_index,
                    'bullet_point_text': bp_text,
                    'questions': bullet_questions,
                    'generation_metadata': {
                        'generated_timestamp': datetime.now().isoformat(),
                        'openai_model': self.model_name,
                        'questions_count': len(bullet_questions),
                        'bullet_point_length': len(bp_text),
                        'options_randomized': True,
                        'api_key_used': api_key_used,
                        'cluster_id': task.cluster_id,
                        'cluster_size': len(task.bullet_point_cluster),
                        'chapter_name': task.chapter_name,
                        'section_number': task.section_number,
                        'processing_method': 'cluster'
                    }
                }
                cluster_results.append(result)

                # Update stats
        self.stats.completed_bullet_points += len(task.bullet_point_cluster)
        self.stats.total_questions_generated += 4  # Always 4 questions per cluster
        self.stats.total_clusters_processed += 1
        
        return True, cluster_results, api_key_used
    
    def create_clean_progress_display(self, current: int, total: int, chapter: str, section: str, cluster_size: int, api_key: str, status: str):
        """Create clean, minimal progress display for clusters"""
        progress_pct = (current / total * 100) if total > 0 else 0
        
        # Truncate long names
        chapter_short = chapter[:18] + "..." if len(chapter) > 21 else chapter
        section_short = f"Sec {section}" if len(section) <= 8 else f"Sec {section[:5]}..."
        cluster_info = f"[{cluster_size}bp]"  # Show bullet points in cluster
        
        if RICH_AVAILABLE:
            status_color = {
                'success': 'green',
                'failed': 'red',
                'processing': 'blue'
            }.get(status, 'white')
            
            console.print(f"[{status_color}]{status.upper():<9}[/{status_color}] "
                         f"[cyan]{current:3d}/{total:<3d}[/cyan] "
                         f"[magenta]{progress_pct:5.1f}%[/magenta] "
                         f"[blue]{chapter_short:<21}[/blue] "
                         f"[green]{section_short:<12}[/green] "
                         f"[white]{cluster_info:<6}[/white] "
                         f"[yellow]{api_key}[/yellow]")
        else:
            print(f"{status.upper():<9} {current:3d}/{total:<3d} {progress_pct:5.1f}% "
                  f"{chapter_short:<21} {section_short:<12} {cluster_info:<6} {api_key}")
    
    def save_updated_file(self, file_path: Path, new_results: List[Dict], original_metadata: Dict):
        """Save or update the question file with new cluster results"""
        try:
            output_file = self.output_dir / f"questions_{file_path.stem}.json"
            
            # Load existing data if file exists
            existing_data = {}
            all_sections = []
            
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                all_sections = existing_data.get('sections', [])
            
            # Organize new results by chapter-section
            new_results_by_section = {}
            for result in new_results:
                metadata = result.get('generation_metadata', {})
                chapter_name = metadata.get('chapter_name', 'Unknown')
                section_number = metadata.get('section_number', 'unknown')
                section_key = f"{chapter_name}_{section_number}"
                
                if section_key not in new_results_by_section:
                    new_results_by_section[section_key] = []
                new_results_by_section[section_key].append(result)
            
            # Update or add sections
            for section_key, new_bullet_points in new_results_by_section.items():
                # Find existing section
                existing_section_index = None
                for i, section in enumerate(all_sections):
                    existing_key = f"{section.get('chapter_name', '')}_{section.get('section_number', '')}"
                    if existing_key == section_key:
                        existing_section_index = i
                        break
                
                if existing_section_index is not None:
                    # Merge bullet points into existing section
                    existing_bullets = all_sections[existing_section_index].get('bullet_points', [])
                    
                    # Add only new bullet points (avoid duplicates)
                    for new_bp in new_bullet_points:
                        bp_index = new_bp.get('bullet_point_index')
                        # Check if already exists
                        exists = any(bp.get('bullet_point_index') == bp_index for bp in existing_bullets)
                        if not exists:
                            existing_bullets.append(new_bp)
                    
                    # Sort by bullet point index
                    existing_bullets.sort(key=lambda x: x.get('bullet_point_index', 0))
                    all_sections[existing_section_index]['bullet_points'] = existing_bullets
                    all_sections[existing_section_index]['total_bullet_points'] = len(existing_bullets)
                else:
                    # Create new section
                    if new_bullet_points:
                        first_bp = new_bullet_points[0]
                        metadata = first_bp.get('generation_metadata', {})
                        
                        new_section = {
                            'chapter_name': metadata.get('chapter_name', 'Unknown Chapter'),
                            'section_name': 'Generated Section',
                            'section_number': metadata.get('section_number', 'unknown'),
                            'source_file': file_path.name,
                            'original_index': len(all_sections),
                            'total_bullet_points': len(new_bullet_points),
                            'bullet_points': sorted(new_bullet_points, key=lambda x: x.get('bullet_point_index', 0))
                        }
                        all_sections.append(new_section)
            
            # Calculate final statistics
            total_sections = len(all_sections)
            total_bullet_points = sum(len(s.get('bullet_points', [])) for s in all_sections)
            total_questions = sum(len(bp.get('questions', [])) for s in all_sections for bp in s.get('bullet_points', []))
            
            # Create completion status
            completion_status = {}
            for section in all_sections:
                chapter_name = section.get('chapter_name', 'Unknown')
                section_number = section.get('section_number', 'unknown')
                section_key = f"{chapter_name}_{section_number}"
                
                bullet_points = section.get('bullet_points', [])
                completed_bullets = [bp.get('bullet_point_index', -1) for bp in bullet_points if bp.get('bullet_point_index', -1) >= 0]
                
                completion_status[section_key] = {
                    'total_bullets': section.get('total_bullet_points', len(bullet_points)),
                    'completed_bullets': sorted(completed_bullets),
                    'completion_percentage': (len(completed_bullets) / max(section.get('total_bullet_points', 1), 1) * 100)
                }
            
            # Create final structure
            final_data = {
                'generation_info': {
                    'source_file': file_path.name,
                    'generation_timestamp': datetime.now().isoformat(),
                    'openai_model': self.model_name,
                    'processing_method': 'cluster',
                    'cluster_size': self.cluster_size,
                    'questions_per_cluster': 4,
                    'total_sections': total_sections,
                    'total_bullet_points': total_bullet_points,
                    'total_questions_generated': total_questions,
                    'source_metadata': original_metadata,
                    'completion_status': completion_status
                },
                'sections': all_sections
            }
            
            # Write atomically using temporary file
            temp_file = output_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            temp_file.rename(output_file)
            
        except Exception as e:
            self.logger.error(f"Failed to save updated file: {e}")
    
    def process_file_with_cluster_resume(self, file_path: Path) -> bool:
        """Process a file using cluster-based resume system"""
        
        # Load original file
        original_data = self.load_extracted_file(file_path)
        if original_data is None:
            return False
        
        # Analyze completion status
        question_file_path = self.output_dir / f"questions_{file_path.stem}.json"
        completion_map = self.analyze_section_completion(original_data, question_file_path)
        
        # Create cluster tasks only for missing bullet points
        cluster_tasks = self.create_cluster_tasks_from_completion_map(file_path, original_data, completion_map)
        
        if not cluster_tasks:
            if RICH_AVAILABLE:
                console.print(f"[green]✓ {file_path.name}: All bullet points already completed[/green]")
            else:
                print(f"✓ {file_path.name}: All bullet points already completed")
            self.stats.completed_files += 1
            return True
        
        # Calculate total bullet points in clusters
        total_cluster_bullets = sum(len(task.bullet_point_cluster) for task in cluster_tasks)
        
        # Show file processing header
        if RICH_AVAILABLE:
            console.print(f"\n[bold blue]Processing: {file_path.name}[/bold blue]")
            console.print(f"[cyan]Found {len(cluster_tasks)} clusters with {total_cluster_bullets} bullet points[/cyan]")
            console.print(f"[magenta]Each cluster generates exactly 4 questions[/magenta]")
            console.print("-" * 95)
            console.print(f"{'STATUS':<9} {'PROGRESS':<7} {'%':<6} {'CHAPTER':<21} {'SECTION':<12} {'CLSTR':<6} {'API'}")
            console.print("-" * 95)
        else:
            print(f"\nProcessing: {file_path.name}")
            print(f"Found {len(cluster_tasks)} clusters with {total_cluster_bullets} bullet points")
            print(f"Each cluster generates exactly 4 questions")
            print("-" * 95)
            print(f"{'STATUS':<9} {'PROGRESS':<7} {'%':<6} {'CHAPTER':<21} {'SECTION':<12} {'CLSTR':<6} {'API'}")
            print("-" * 95)
        
        # Process cluster tasks in parallel
        processed_count = 0
        total_tasks = len(cluster_tasks)
        all_completed_results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all cluster tasks
            future_to_task = {executor.submit(self.process_cluster_task, task): task for task in cluster_tasks}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    success, cluster_results, api_key = future.result()
                    processed_count += 1
                    
                    if success:
                        all_completed_results.extend(cluster_results)
                        self.create_clean_progress_display(
                            processed_count, total_tasks,
                            task.chapter_name, task.section_number,
                            len(task.bullet_point_cluster), api_key, 'success'
                        )
                    else:
                        self.create_clean_progress_display(
                            processed_count, total_tasks,
                            task.chapter_name, task.section_number,
                            len(task.bullet_point_cluster), api_key, 'failed'
                        )
                        
                except Exception as e:
                    processed_count += 1
                    self.create_clean_progress_display(
                        processed_count, total_tasks,
                        task.chapter_name, task.section_number,
                        len(task.bullet_point_cluster), 'error', 'failed'
                    )
                    self.logger.error(f"Cluster task failed: {e}")
                
                # Save progress periodically (every 5 clusters)
                if len(all_completed_results) > 0 and processed_count % 5 == 0:
                    self.save_updated_file(file_path, all_completed_results, original_data.get('metadata', {}))
        
        # Final save with all results
        if all_completed_results:
            self.save_updated_file(file_path, all_completed_results, original_data.get('metadata', {}))
        
        self.stats.completed_files += 1
        return True
    
    def create_master_question_bank(self, processed_files: List[Path]):
        """Create master question bank with all questions"""
        all_sections = []
        total_questions = 0
        total_clusters = 0
        
        for file_path in processed_files:
            question_file = self.output_dir / f"questions_{file_path.stem}.json"
            if question_file.exists():
                try:
                    with open(question_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    sections = data.get('sections', [])
                    all_sections.extend(sections)
                    
                    # Count questions and estimate clusters
                    for section in sections:
                        for bp in section.get('bullet_points', []):
                            questions = bp.get('questions', [])
                            total_questions += len(questions)
                            # Each cluster generates 4 questions, estimate clusters
                            if len(questions) > 0:
                                metadata = bp.get('generation_metadata', {})
                                if metadata.get('processing_method') == 'cluster':
                                    total_clusters += 1
                    
                except Exception as e:
                    self.logger.error(f"Error reading question file {question_file}: {e}")
        
        if all_sections:
            master_data = {
                'master_question_bank_info': {
                    'creation_timestamp': datetime.now().isoformat(),
                    'total_sections': len(all_sections),
                    'total_questions': total_questions,
                    'total_clusters_processed': total_clusters,
                    'processing_method': 'cluster',
                    'cluster_size': self.cluster_size,
                    'questions_per_cluster': 4,
                    'source_folder': str(self.folder_path),
                    'openai_model': self.model_name
                },
                'sections': all_sections
            }
            
            master_file = self.output_dir / "master_question_bank.json"
            with open(master_file, 'w', encoding='utf-8') as f:
                json.dump(master_data, f, indent=2, ensure_ascii=False)
            
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Master question bank created with {total_questions} questions from {total_clusters} clusters[/green]")
            else:
                print(f"✓ Master question bank created with {total_questions} questions from {total_clusters} clusters")
    
    def show_api_usage_summary(self):
        """Display clean API usage summary"""
        usage_summary = self.api_manager.get_usage_summary()
        
        if RICH_AVAILABLE:
            console.print("\n" + "="*70)
            console.print("[bold]API Usage Summary[/bold]")
            console.print("="*70)
            
            table = Table()
            table.add_column("API Key", style="cyan")
            table.add_column("Clusters", style="green", justify="right")
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
            console.print(f"[bold]Total Cluster API Calls:[/bold] {usage_summary['total_requests']}")
            console.print(f"[bold]Total Errors:[/bold] {usage_summary['total_errors']}")
            console.print(f"[bold]Estimated Questions:[/bold] {usage_summary['total_requests'] * 4}")
            console.print("="*70)
        else:
            print("\n" + "="*70)
            print("API Usage Summary")
            print("="*70)
            for key_name, requests in usage_summary['usage_stats'].items():
                errors = usage_summary['error_counts'][key_name]
                success_rate = ((requests - errors) / requests * 100) if requests > 0 else 0
                print(f"{key_name}: {requests} clusters, {errors} errors, {success_rate:.1f}% success")
            print(f"Total Cluster API Calls: {usage_summary['total_requests']}")
            print(f"Total Errors: {usage_summary['total_errors']}")
            print(f"Estimated Questions: {usage_summary['total_requests'] * 4}")
            print("="*70)
    
    def run_generation(self) -> bool:
        """Main method to run the cluster-based MCQ generation process"""
        
        # Show startup info
        if RICH_AVAILABLE:
            startup_panel = Panel.fit(
                f"[bold]Cluster-Based UPSC MCQ Generator[/bold]\n"
                f"Model: [cyan]{self.model_name}[/cyan]\n"
                f"API Keys: [green]{len(self.api_manager.api_keys)}[/green]\n"
                f"Workers: [yellow]{self.max_workers}[/yellow]\n"
                f"Cluster Size: [magenta]{self.cluster_size} bullet points[/magenta]\n"
                f"Questions per Cluster: [blue]4 questions[/blue]",
                title="Configuration",
                border_style="blue"
            )
            console.print(startup_panel)
        else:
            print("="*60)
            print("Cluster-Based UPSC MCQ Generator")
            print(f"Model: {self.model_name}")
            print(f"API Keys: {len(self.api_manager.api_keys)}")
            print(f"Workers: {self.max_workers}")
            print(f"Cluster Size: {self.cluster_size} bullet points")
            print(f"Questions per Cluster: 4 questions")
            print("="*60)
        
        # Discover files
        extracted_files = self.discover_extracted_files()
        if not extracted_files:
            if RICH_AVAILABLE:
                console.print("[red]✗ No extracted JSON files found to process[/red]")
            else:
                print("✗ No extracted JSON files found to process")
            return False
        
        # Analyze completion status across all files
        completion_maps = {}
        for file_path in extracted_files:
            original_data = self.load_extracted_file(file_path)
            if original_data:
                question_file_path = self.output_dir / f"questions_{file_path.stem}.json"
                completion_maps[file_path.name] = self.analyze_section_completion(original_data, question_file_path)
        
        # Show resume info
        self.show_resume_info(completion_maps)
        
        # Process files
        processed_files = []
        for file_path in extracted_files:
            try:
                if self.process_file_with_cluster_resume(file_path):
                    processed_files.append(file_path)
            except KeyboardInterrupt:
                if RICH_AVAILABLE:
                    console.print("\n[yellow]⚠ Process interrupted. All progress saved automatically.[/yellow]")
                else:
                    print("\n⚠ Process interrupted. All progress saved automatically.")
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
        if RICH_AVAILABLE:
            summary_panel = Panel.fit(
                f"[bold green]✓ Cluster-Based UPSC MCQ Generation Complete[/bold green]\n\n"
                f"[bold]Files Processed:[/bold] {self.stats.completed_files}\n"
                f"[bold]Sections Completed:[/bold] {self.stats.completed_sections}\n"
                f"[bold]Bullet Points Processed:[/bold] {self.stats.completed_bullet_points}\n"
                f"[bold]Clusters Processed:[/bold] {self.stats.total_clusters_processed}\n"
                f"[bold]Failed Bullet Points:[/bold] {self.stats.failed_bullet_points}\n"
                f"[bold]UPSC Questions Generated:[/bold] {self.stats.total_questions_generated}\n"
                f"[bold]Efficiency:[/bold] ~{self.stats.total_questions_generated/max(self.stats.total_clusters_processed,1):.1f} questions per API call\n\n"
                f"[bold]Output Location:[/bold] {self.output_dir}",
                title="Final Summary",
                border_style="green"
            )
            console.print(summary_panel)
        else:
            print("\n" + "="*60)
            print("✓ Cluster-Based UPSC MCQ Generation Complete")
            print("="*60)
            print(f"Files Processed: {self.stats.completed_files}")
            print(f"Sections Completed: {self.stats.completed_sections}")
            print(f"Bullet Points Processed: {self.stats.completed_bullet_points}")
            print(f"Clusters Processed: {self.stats.total_clusters_processed}")
            print(f"Failed Bullet Points: {self.stats.failed_bullet_points}")
            print(f"UPSC Questions Generated: {self.stats.total_questions_generated}")
            print(f"Efficiency: ~{self.stats.total_questions_generated/max(self.stats.total_clusters_processed,1):.1f} questions per API call")
            print(f"Output Location: {self.output_dir}")
            print("="*60)

def main():
    """Main entry point"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Cluster-Based UPSC MCQ Question Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cluster_mcq_generator.py /path/to/extracted/folder
  python cluster_mcq_generator.py /path/to/extracted/folder --model gpt-4
  python cluster_mcq_generator.py /path/to/extracted/folder --cluster-size 2 --workers 6

Environment Variables:
  OPENAI_API_KEY      - Primary API key  
  OPENAI_API_KEY_1    - Additional API key 1
  OPENAI_API_KEY_2    - Additional API key 2
  ... and so on (no limit)

Features:
  - Processes bullet points in clusters of 2-3 for efficiency  
  - Generates exactly 4 questions per cluster
  - Robust chapter-section based resume functionality
  - UPSC-style analytical questions with randomized options
  - Smart load balancing across multiple API keys
  - Perfect resume from any interruption point
        """
    )
    
    parser.add_argument('folder_path', help='Path to folder containing extracted Wikipedia JSON files')
    parser.add_argument('--model', default='gpt-4.1-mini', help='OpenAI model to use (default: gpt-4.1-mini)')
    parser.add_argument('--cluster-size', type=int, default=3, choices=[2, 3], help='Bullet points per cluster (2-3, default: 3)')
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
        generator = ClusterMCQGenerator(
            folder_path=str(folder_path),
            model_name=args.model,
            cluster_size=getattr(args, 'cluster_size', 3),
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