#!/usr/bin/env python3
"""
Wikipedia JSON Validation System (Enhanced)
Validates processed Wikipedia JSON files by checking if all sections have been enhanced with OpenAI summaries.
Provides detailed reports on completion status, including section number, chapter name, and section name for missing parts.
"""

import json
from pathlib import Path
import argparse
import sys

class WikipediaValidationManager:
    """
    Manager class for validating enhanced Wikipedia JSON files
    """
    
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.total_files = 0
        self.completed_files = 0
        self.incomplete_files = 0
        self.incomplete_details = {}  # file -> list of dicts with missing section info
    
    def discover_json_files(self) -> list[Path]:
        """Discover all JSON files in the target folder"""
        json_files = list(self.folder_path.glob("*.json"))
        self.total_files = len(json_files)
        return sorted(json_files)
    
    def check_section_processed(self, section: dict) -> bool:
        """Check if section has been processed with non-empty summarised points"""
        return ('openai_summarised_points' in section and 
                isinstance(section.get('openai_summarised_points'), list) and 
                len(section.get('openai_summarised_points', [])) > 0)
    
    def validate_file(self, file_path: Path) -> tuple[bool, list[dict]]:
        """Validate a single JSON file and collect detailed missing section info"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"❌ Invalid structure in {file_path.name}: Expected list of sections")
                return False, [{"error": "Invalid JSON structure"}]
            
            missing_sections = []
            for i, section in enumerate(data):
                if not self.check_section_processed(section):
                    section_number = section.get('section_number', f"section_{i}")
                    section_name = section.get('section_name', "Untitled")
                    chapter_name = section.get('chapter_name', "No Chapter")
                    missing_sections.append({
                        "section_number": section_number,
                        "chapter_name": chapter_name,
                        "section_name": section_name
                    })
            
            return len(missing_sections) == 0, missing_sections
        
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {file_path.name}")
            return False, [{"error": "JSON decode error"}]
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
            return False, [{"error": str(e)}]
    
    def run_validation(self):
        """Run validation on all files"""
        print(f"\n🔍 Starting validation for folder: {self.folder_path}")
        json_files = self.discover_json_files()
        
        if not json_files:
            print("⚠️ No JSON files found in the folder.")
            return
        
        print(f"📁 Found {self.total_files} JSON files to validate.\n")
        
        for file_path in json_files:
            is_complete, missing = self.validate_file(file_path)
            
            if is_complete:
                self.completed_files += 1
                print(f"✅ {file_path.name}: Fully complete")
            else:
                self.incomplete_files += 1
                self.incomplete_details[file_path.name] = missing
                print(f"❌ {file_path.name}: Incomplete")
                if missing and "error" not in missing[0]:
                    print("   Missing sections:")
                    for sec in missing:
                        print(f"     - Section Number: {sec['section_number']}")
                        print(f"       Chapter: {sec['chapter_name']}")
                        print(f"       Section Name: {sec['section_name']}")
                        print("")
                elif missing:
                    print("   Error:", missing[0].get("error"))
                print("")
        
        self.print_summary()
    
    def print_summary(self):
        """Print overall summary"""
        print("\n📊 Validation Summary")
        print("====================")
        print(f"Total files: {self.total_files}")
        print(f"Completed files: {self.completed_files}")
        print(f"Incomplete files: {self.incomplete_files}")
        
        if self.incomplete_files > 0:
            print("\nIncomplete Files Details:")
            for file, missing in self.incomplete_details.items():
                if "error" not in missing[0]:
                    print(f"- {file}: {len(missing)} missing sections")
                else:
                    print(f"- {file}: Error - {missing[0].get('error')}")
        
        completion_rate = (self.completed_files / self.total_files * 100) if self.total_files > 0 else 0
        print(f"\nCompletion rate: {completion_rate:.2f}%")
        print("====================")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Wikipedia JSON Validation System (Enhanced)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python validate_wikipedia_enhanced.py /path/to/json/folder"
    )
    
    parser.add_argument(
        'folder_path',
        nargs='?',
        help='Path to folder containing processed Wikipedia JSON files. If not provided, will prompt for input.'
    )
    
    args = parser.parse_args()
    
    folder_path = args.folder_path
    if not folder_path:
        folder_path = input("📂 Enter the path to the folder containing JSON files: ").strip()
    
    if not folder_path:
        print("❌ No folder path provided.")
        sys.exit(1)
    
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"❌ Invalid folder path: {folder_path}")
        sys.exit(1)
    
    validator = WikipediaValidationManager(str(path))
    validator.run_validation()

if __name__ == "__main__":
    main()