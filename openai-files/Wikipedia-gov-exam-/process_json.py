#!/usr/bin/env python3
"""
Wikipedia JSON Enhancement System
Processes Wikipedia JSON files to add detailed AI-generated summaries.
Supports smart resume functionality and comprehensive logging.
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import argparse
from dataclasses import dataclass, asdict
from openai import OpenAI
from dotenv import load_dotenv

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
    """Statistics for tracking processing progress"""
    total_files: int = 0
    completed_files: int = 0
    skipped_files: int = 0
    total_sections: int = 0
    completed_sections: int = 0
    skipped_sections: int = 0
    failed_sections: int = 0
    start_time: Optional[str] = None
    last_update_time: Optional[str] = None

@dataclass
class ProcessingState:
    """State information for resume functionality"""
    folder_path: str
    last_processed_file: Optional[str] = None
    last_processed_section: Optional[str] = None
    timestamp: Optional[str] = None
    stats: ProcessingStats = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = ProcessingStats()

class WikipediaEnhancementManager:
    """
    Main manager class that orchestrates the entire enhancement process
    """
    
    def __init__(self, folder_path: str, api_key: str, model_name: str = "gpt-4.1-mini"):
        self.folder_path = Path(folder_path)
        self.model_name = model_name
        
        # Initialize OpenAI client
        try:
            self.client = OpenAI(api_key=api_key)
            console.print("[green]✓ OpenAI client initialized successfully[/green]")
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize OpenAI client: {e}[/red]")
            sys.exit(1)
        
        # Setup directories
        self.logs_dir = self.folder_path.parent / "logs"
        self.backups_dir = self.folder_path.parent / "backups"
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Initialize state
        self.state_file = self.logs_dir / "processing_state.json"
        self.processing_state = self.load_processing_state()
        
        # Statistics
        self.start_time = datetime.now()
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Main logger
        self.logger = logging.getLogger('WikipediaEnhancer')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handlers
        master_handler = logging.FileHandler(self.logs_dir / 'master_processing.log')
        master_handler.setFormatter(logging.Formatter(log_format))
        master_handler.setLevel(logging.INFO)
        
        section_handler = logging.FileHandler(self.logs_dir / 'section_processing.log')
        section_handler.setFormatter(logging.Formatter(log_format))
        section_handler.setLevel(logging.DEBUG)
        
        # Console handler
        if RICH_AVAILABLE:
            console_handler = RichHandler(console=console, rich_tracebacks=True)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        
        console_handler.setLevel(logging.INFO)
        
        # Add handlers
        self.logger.addHandler(master_handler)
        self.logger.addHandler(section_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("Logging system initialized")
    
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
    
    def discover_json_files(self) -> List[Path]:
        """Discover all JSON files in the target folder"""
        self.logger.info(f"Discovering JSON files in {self.folder_path}")
        
        try:
            json_files = list(self.folder_path.glob("*.json"))
            self.logger.info(f"Discovered {len(json_files)} JSON files")
            self.processing_state.stats.total_files = len(json_files)
            return sorted(json_files)
        except Exception as e:
            self.logger.error(f"Failed to discover JSON files: {e}")
            return []
    
    def load_json_file(self, file_path: Path) -> Optional[List[Dict]]:
        """Load and validate JSON file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                self.logger.error(f"Invalid JSON structure in {file_path}: expected list")
                return None
                
            self.logger.debug(f"Loaded {len(data)} sections from {file_path}")
            return data
            
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def save_json_file(self, data: List[Dict], file_path: Path) -> bool:
        """Save updated JSON data to file"""
        try:
            # Create backup first
            backup_path = self.backups_dir / f"{file_path.stem}_backup_{int(time.time())}.json"
            if file_path.exists():
                import shutil
                shutil.copy2(file_path, backup_path)
            
            # Save updated data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Saved updated JSON to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save JSON file {file_path}: {e}")
            return False
    
    def check_section_processed(self, section: Dict) -> bool:
        """Check if section has already been processed"""
        return ('openai_summarised_points' in section and 
                isinstance(section.get('openai_summarised_points'), list) and 
                len(section.get('openai_summarised_points', [])) > 0)
    
    def call_openai_api(self, content: str, chapter_name: str = "", section_name: str = "") -> Optional[List[str]]:
        """Call OpenAI API to generate detailed bullet point summary"""
        
        system_message = """You are an expert academic content summarizer specializing in creating comprehensive, detailed bullet points that preserve all important information from source material."""
        
        context_info = ""
        if chapter_name and section_name:
            context_info = f"\nCHAPTER: {chapter_name}\nSECTION: {section_name}\n"
        
        user_prompt = f"""Create a detailed bullet point summary of the following Wikipedia section content.{context_info}

REQUIREMENTS:
- Cover ALL key details, facts, statistics, dates, names, and concepts mentioned
- Each bullet point should be comprehensive and standalone
- Preserve specific numbers, percentages, monetary values, and dates exactly
- Include all mentioned organizations, people, and place names
- Don't omit any substantial information from the original text
- Use clear, academic language suitable for study materials
- Format as bullet points starting with '•'
- Ensure bullet points flow logically and cover the entire content scope

CONTENT TO SUMMARIZE:
{content}

Return ONLY the bullet points, nothing else:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent summaries
                max_tokens=2000   # Enough for detailed summaries
            )
            
            if response.choices and response.choices[0].message:
                content_response = response.choices[0].message.content.strip()
                
                # Parse bullet points
                bullet_points = []
                for line in content_response.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                        # Normalize bullet point format
                        clean_point = line.lstrip('•-*').strip()
                        if clean_point:
                            bullet_points.append(f"• {clean_point}")
                
                return bullet_points if bullet_points else None
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None
    
    def process_section(self, section: Dict, file_path: Path) -> bool:
        """Process a single section and update it with AI summary"""
        section_id = f"{section.get('section_number', 'unknown')}"
        section_name = section.get('section_name', 'Untitled')
        
        # Check if already processed
        if self.check_section_processed(section):
            self.logger.debug(f"SKIPPED - Already processed: {section_id} - {section_name}")
            self.processing_state.stats.skipped_sections += 1
            return True
        
        # Get content - handle both field names
        content = section.get('generated_section_content_md', '') or section.get('text', '')
        if not content or len(content.strip()) < 50:  # Skip very short content
            self.logger.warning(f"SKIPPED - Insufficient content: {section_id} - {section_name}")
            self.processing_state.stats.skipped_sections += 1
            return True
        
        self.logger.info(f"PROCESSING: {section_id} - {section_name} ({len(content)} chars)")
        
        # Call OpenAI API with retries
        bullet_points = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                bullet_points = self.call_openai_api(
                    content, 
                    section.get('chapter_name', ''), 
                    section_name
                )
                if bullet_points:
                    break
                else:
                    self.logger.warning(f"Empty response from API, attempt {attempt + 1}/{max_retries}")
            except Exception as e:
                self.logger.warning(f"API call failed, attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        if not bullet_points:
            self.logger.error(f"FAILED - Could not process: {section_id} - {section_name}")
            self.processing_state.stats.failed_sections += 1
            return False
        
        # Update section with AI summary
        section['openai_summarised_points'] = bullet_points
        section['processing_metadata'] = {
            'processed_timestamp': datetime.now().isoformat(),
            'openai_model': self.model_name,
            'content_length': len(content),
            'bullet_points_count': len(bullet_points)
        }
        
        self.logger.info(f"SUCCESS: {section_id} - Generated {len(bullet_points)} bullet points")
        self.processing_state.stats.completed_sections += 1
        
        # Update processing state
        self.processing_state.last_processed_file = file_path.name
        self.processing_state.last_processed_section = section_id
        
        return True
    
    def process_file(self, file_path: Path) -> bool:
        """Process all sections in a single JSON file"""
        self.logger.info(f"PROCESSING FILE: {file_path.name}")
        
        # Load file
        data = self.load_json_file(file_path)
        if data is None:
            self.logger.error(f"Failed to load file: {file_path}")
            return False
        
        # Count sections
        total_sections = len(data)
        unprocessed_sections = [s for s in data if not self.check_section_processed(s)]
        
        self.logger.info(f"File contains {total_sections} sections, {len(unprocessed_sections)} need processing")
        
        if not unprocessed_sections:
            self.logger.info("All sections already processed, skipping file")
            self.processing_state.stats.skipped_files += 1
            return True
        
        # Process sections with progress tracking
        processed_count = 0
        failed_count = 0
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"Processing {file_path.name}", total=len(unprocessed_sections))
                
                for i, section in enumerate(data):
                    if not self.check_section_processed(section):
                        section_id = section.get('section_number', f'section_{i}')
                        progress.update(task, description=f"Processing {section_id}")
                        
                        if self.process_section(section, file_path):
                            processed_count += 1
                            # Save file immediately after each successful processing
                            self.save_json_file(data, file_path)
                            self.save_processing_state()
                        else:
                            failed_count += 1
                        
                        progress.advance(task)
                        time.sleep(0.5)  # Rate limiting
        else:
            # Fallback without rich progress
            for i, section in enumerate(data):
                if not self.check_section_processed(section):
                    print(f"Processing section {i+1}/{len(unprocessed_sections)}")
                    
                    if self.process_section(section, file_path):
                        processed_count += 1
                        # Save file immediately after each successful processing
                        self.save_json_file(data, file_path)
                        self.save_processing_state()
                    else:
                        failed_count += 1
                    
                    time.sleep(0.5)  # Rate limiting
        
        # Final save
        if processed_count > 0:
            self.save_json_file(data, file_path)
        
        self.logger.info(f"FILE COMPLETE: {file_path.name} - Processed: {processed_count}, Failed: {failed_count}")
        self.processing_state.stats.completed_files += 1
        
        return True
    
    def run_enhancement(self) -> bool:
        """Main method to run the enhancement process"""
        self.logger.info("=== STARTING WIKIPEDIA ENHANCEMENT PROCESS ===")
        self.logger.info(f"Target folder: {self.folder_path}")
        self.logger.info(f"OpenAI model: {self.model_name}")
        
        # Discover files
        json_files = self.discover_json_files()
        if not json_files:
            self.logger.error("No JSON files found to process")
            return False
        
        # Process files
        console.print(f"\n[bold]Processing {len(json_files)} JSON files...[/bold]\n")
        
        for file_path in json_files:
            try:
                self.process_file(file_path)
            except KeyboardInterrupt:
                self.logger.info("Process interrupted by user")
                self.save_processing_state()
                console.print("\n[yellow]Process interrupted. State saved. Resume with the same command.[/yellow]")
                return False
            except Exception as e:
                self.logger.error(f"Critical error processing {file_path}: {e}")
                continue
        
        # Final statistics
        self.print_final_report()
        self.logger.info("=== ENHANCEMENT PROCESS COMPLETE ===")
        return True
    
    def print_final_report(self):
        """Print comprehensive final report"""
        stats = self.processing_state.stats
        duration = datetime.now() - datetime.fromisoformat(stats.start_time) if stats.start_time else None
        
        console.print("\n" + "="*60)
        console.print("[bold]PROCESSING COMPLETE - FINAL REPORT[/bold]")
        console.print("="*60)
        
        console.print(f"[bold]Files:[/bold]")
        console.print(f"  Total files: {stats.total_files}")
        console.print(f"  Completed files: {stats.completed_files}")
        console.print(f"  Skipped files: {stats.skipped_files}")
        
        console.print(f"\n[bold]Sections:[/bold]")
        console.print(f"  Total sections processed: {stats.completed_sections}")
        console.print(f"  Sections skipped: {stats.skipped_sections}")
        console.print(f"  Sections failed: {stats.failed_sections}")
        
        if duration:
            console.print(f"\n[bold]Performance:[/bold]")
            console.print(f"  Total duration: {duration}")
            if stats.completed_sections > 0:
                rate = stats.completed_sections / duration.total_seconds() * 60
                console.print(f"  Processing rate: {rate:.2f} sections/minute")
        
        console.print(f"\n[bold]Logs saved to:[/bold] {self.logs_dir}")
        console.print("="*60)

def main():
    """Main entry point"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Wikipedia JSON Enhancement System with AI Summaries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhance_wikipedia.py /path/to/json/folder
  python enhance_wikipedia.py /path/to/json/folder --model gpt-3.5-turbo
  python enhance_wikipedia.py /path/to/json/folder --api-key your-key-here
        """
    )
    
    parser.add_argument(
        'folder_path',
        help='Path to folder containing Wikipedia JSON files'
    )
    
    parser.add_argument(
        '--api-key',
        default=os.getenv('OPENAI_API_KEY'),
        help='OpenAI API key (defaults to OPENAI_API_KEY env var)'
    )
    
    parser.add_argument(
        '--model',
        default='gpt-4.1-mini',
        help='OpenAI model to use (default: gpt-4.1-mini)'
    )
    

    
    args = parser.parse_args()
    
    # Validate API key
    if not args.api_key:
        print("❌ Error: OpenAI API key not found. Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Validate folder path
    folder_path = Path(args.folder_path)
    if not folder_path.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"❌ Error: Path is not a directory: {folder_path}")
        sys.exit(1)
    
    # Initialize manager and run
    try:
        manager = WikipediaEnhancementManager(
            folder_path=str(folder_path),
            api_key=args.api_key,
            model_name=args.model
        )
        
        success = manager.run_enhancement()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()