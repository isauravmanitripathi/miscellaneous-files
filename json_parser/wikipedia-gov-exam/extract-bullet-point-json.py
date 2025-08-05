#!/usr/bin/env python3
"""
Wikipedia JSON Field Extractor
Extracts specific fields from enhanced Wikipedia JSON files and creates clean, structured output.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import argparse

# Rich library for better console output (optional)
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    class SimpleConsole:
        def print(self, text, **kwargs):
            print(text)
    console = SimpleConsole()
    RICH_AVAILABLE = False

class WikipediaJSONExtractor:
    """
    Extracts specific fields from Wikipedia JSON files and creates clean output
    """
    
    def __init__(self, input_folder: str, output_folder: str = None):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder) if output_folder else self.input_folder.parent / "extracted_data"
        
        # Validate input folder
        if not self.input_folder.exists():
            raise ValueError(f"Input folder does not exist: {self.input_folder}")
        if not self.input_folder.is_dir():
            raise ValueError(f"Input path is not a directory: {self.input_folder}")
        
        # Create output folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_sections': 0,
            'extracted_sections': 0,
            'skipped_sections': 0,
            'start_time': datetime.now()
        }
        
        console.print(f"[green]✓ Input folder: {self.input_folder}[/green]")
        console.print(f"[green]✓ Output folder: {self.output_folder}[/green]")
    
    def discover_json_files(self) -> List[Path]:
        """Discover all JSON files in the input folder"""
        console.print("[blue]Discovering JSON files...[/blue]")
        
        json_files = list(self.input_folder.glob("*.json"))
        self.stats['total_files'] = len(json_files)
        
        console.print(f"[green]✓ Found {len(json_files)} JSON files[/green]")
        return sorted(json_files)
    
    def extract_section_data(self, section: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract required fields from a section"""
        
        # Check if section has OpenAI summarized points
        openai_points = section.get('openai_summarised_points')
        if not openai_points or not isinstance(openai_points, list) or len(openai_points) == 0:
            return None  # Skip sections without AI summaries
        
        # Extract fields with fallbacks
        extracted_data = {
            'section_number': section.get('section_number', 'unknown'),
            'section_name': section.get('section_name', 'Untitled'),
            'chapter_name': section.get('chapter_name', 'Unknown Chapter'),
            'chapter_id': section.get('chapter_id', section.get('chapter_number', 'unknown')),
            'openai_summarised_points': openai_points
        }
        
        # Add optional metadata if available
        if 'processing_metadata' in section:
            metadata = section['processing_metadata']
            extracted_data['metadata'] = {
                'processed_timestamp': metadata.get('processed_timestamp'),
                'openai_model': metadata.get('openai_model'),
                'bullet_points_count': metadata.get('bullet_points_count', len(openai_points))
            }
        else:
            # Create basic metadata
            extracted_data['metadata'] = {
                'bullet_points_count': len(openai_points),
                'extraction_timestamp': datetime.now().isoformat()
            }
        
        return extracted_data
    
    def process_json_file(self, file_path: Path) -> bool:
        """Process a single JSON file and extract data"""
        console.print(f"[blue]Processing: {file_path.name}[/blue]")
        
        try:
            # Load JSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                console.print(f"[red]✗ Invalid JSON structure in {file_path.name}: expected list[/red]")
                return False
            
            # Extract sections
            extracted_sections = []
            sections_processed = 0
            sections_skipped = 0
            
            for i, section in enumerate(data):
                self.stats['total_sections'] += 1
                
                extracted = self.extract_section_data(section)
                if extracted:
                    # Add source information
                    extracted['source_file'] = file_path.name
                    extracted['original_index'] = i
                    
                    extracted_sections.append(extracted)
                    sections_processed += 1
                    self.stats['extracted_sections'] += 1
                else:
                    sections_skipped += 1
                    self.stats['skipped_sections'] += 1
            
            # Save extracted data if any sections were processed
            if extracted_sections:
                output_file = self.output_folder / f"extracted_{file_path.name}"
                
                # Create summary metadata
                file_summary = {
                    'extraction_info': {
                        'source_file': file_path.name,
                        'extraction_timestamp': datetime.now().isoformat(),
                        'total_sections_in_source': len(data),
                        'extracted_sections_count': len(extracted_sections),
                        'skipped_sections_count': sections_skipped
                    },
                    'sections': extracted_sections
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(file_summary, f, indent=2, ensure_ascii=False)
                
                console.print(f"[green]✓ Extracted {sections_processed} sections from {file_path.name}[/green]")
                if sections_skipped > 0:
                    console.print(f"[yellow]  ⚠ Skipped {sections_skipped} sections (no AI summaries)[/yellow]")
            else:
                console.print(f"[yellow]⚠ No valid sections found in {file_path.name}[/yellow]")
            
            self.stats['processed_files'] += 1
            return True
            
        except json.JSONDecodeError as e:
            console.print(f"[red]✗ Invalid JSON in {file_path.name}: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Error processing {file_path.name}: {e}[/red]")
            return False
    
    def create_master_index(self, json_files: List[Path]):
        """Create a master index file with all extracted data"""
        console.print("[blue]Creating master index...[/blue]")
        
        master_data = {
            'extraction_summary': {
                'extraction_timestamp': datetime.now().isoformat(),
                'source_folder': str(self.input_folder),
                'total_files_processed': self.stats['processed_files'],
                'total_sections_extracted': self.stats['extracted_sections'],
                'total_sections_skipped': self.stats['skipped_sections']
            },
            'files': []
        }
        
        # Collect data from all extracted files
        for json_file in json_files:
            extracted_file = self.output_folder / f"extracted_{json_file.name}"
            if extracted_file.exists():
                try:
                    with open(extracted_file, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                    
                    master_data['files'].append({
                        'filename': json_file.name,
                        'extracted_filename': extracted_file.name,
                        'sections_count': len(file_data.get('sections', [])),
                        'extraction_info': file_data.get('extraction_info', {})
                    })
                except Exception as e:
                    console.print(f"[red]✗ Error reading extracted file {extracted_file.name}: {e}[/red]")
        
        # Save master index
        master_file = self.output_folder / "master_index.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓ Master index created: {master_file}[/green]")
    
    def create_flat_dataset(self):
        """Create a flat dataset with all sections in one file"""
        console.print("[blue]Creating flat dataset...[/blue]")
        
        all_sections = []
        
        # Collect all sections from extracted files
        for extracted_file in self.output_folder.glob("extracted_*.json"):
            try:
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                sections = file_data.get('sections', [])
                all_sections.extend(sections)
                
            except Exception as e:
                console.print(f"[red]✗ Error reading {extracted_file.name}: {e}[/red]")
        
        if all_sections:
            flat_dataset = {
                'dataset_info': {
                    'creation_timestamp': datetime.now().isoformat(),
                    'total_sections': len(all_sections),
                    'source_folder': str(self.input_folder),
                    'description': 'Flat dataset containing all extracted Wikipedia sections with AI summaries'
                },
                'sections': all_sections
            }
            
            flat_file = self.output_folder / "flat_dataset.json"
            with open(flat_file, 'w', encoding='utf-8') as f:
                json.dump(flat_dataset, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✓ Flat dataset created with {len(all_sections)} sections: {flat_file}[/green]")
    
    def print_statistics(self):
        """Print final processing statistics"""
        duration = datetime.now() - self.stats['start_time']
        
        if RICH_AVAILABLE:
            table = Table(title="Extraction Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="green")
            
            table.add_row("Total Files Found", str(self.stats['total_files']))
            table.add_row("Files Processed", str(self.stats['processed_files']))
            table.add_row("Total Sections Found", str(self.stats['total_sections']))
            table.add_row("Sections Extracted", str(self.stats['extracted_sections']))
            table.add_row("Sections Skipped", str(self.stats['skipped_sections']))
            table.add_row("Processing Time", str(duration).split('.')[0])
            
            console.print(table)
        else:
            print("\n" + "="*50)
            print("EXTRACTION STATISTICS")
            print("="*50)
            print(f"Total Files Found: {self.stats['total_files']}")
            print(f"Files Processed: {self.stats['processed_files']}")
            print(f"Total Sections Found: {self.stats['total_sections']}")
            print(f"Sections Extracted: {self.stats['extracted_sections']}")
            print(f"Sections Skipped: {self.stats['skipped_sections']}")
            print(f"Processing Time: {duration}")
            print("="*50)
    
    def run_extraction(self) -> bool:
        """Main method to run the extraction process"""
        console.print("\n[bold]Wikipedia JSON Field Extractor[/bold]")
        console.print("="*50)
        
        # Discover files
        json_files = self.discover_json_files()
        if not json_files:
            console.print("[red]✗ No JSON files found to process[/red]")
            return False
        
        # Process files with progress bar
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Extracting data...", total=len(json_files))
                
                for json_file in json_files:
                    self.process_json_file(json_file)
                    progress.advance(task)
        else:
            for i, json_file in enumerate(json_files, 1):
                print(f"Processing {i}/{len(json_files)}: {json_file.name}")
                self.process_json_file(json_file)
        
        # Create master index and flat dataset
        self.create_master_index(json_files)
        self.create_flat_dataset()
        
        # Print statistics
        self.print_statistics()
        
        console.print(f"\n[bold green]✓ Extraction complete! Output saved to: {self.output_folder}[/bold green]")
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Extract specific fields from Wikipedia JSON files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_wikipedia_fields.py /path/to/enhanced/json/folder
  python extract_wikipedia_fields.py /path/to/enhanced/json/folder --output /path/to/output
  
This program extracts:
  - section_number
  - section_name  
  - chapter_name
  - chapter_id
  - openai_summarised_points
  
Only sections with AI summaries are included in the output.
        """
    )
    
    parser.add_argument(
        'input_folder',
        help='Path to folder containing enhanced Wikipedia JSON files'
    )
    
    parser.add_argument(
        '--output',
        help='Output folder path (default: input_folder/../extracted_data)'
    )
    
    args = parser.parse_args()
    
    try:
        extractor = WikipediaJSONExtractor(
            input_folder=args.input_folder,
            output_folder=args.output
        )
        
        success = extractor.run_extraction()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Process interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()