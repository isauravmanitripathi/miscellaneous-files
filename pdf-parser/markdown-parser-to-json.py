#!/usr/bin/env python3
"""
Efficient Markdown Parser
Parse markdown file and create structured JSON with headings, subheadings, and text
"""

import re
import json
from typing import List, Dict
from pathlib import Path

def clean_text(text: str) -> str:
    """Clean markdown text and remove formatting"""
    if not text:
        return ""
    
    # Remove bold/italic markdown
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* -> italic
    
    # Clean up LaTeX math expressions (keep content, remove LaTeX)
    text = re.sub(r'\$([^$]+)\$', r'\1', text)      # $math$ -> math
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def determine_content_type(line: str) -> tuple:
    """
    Determine content type and extract text from markdown line
    Returns: (content_type, cleaned_text)
    """
    line = line.strip()
    
    if not line:
        return None, ""
    
    # Main headings (H1, H2)
    if line.startswith('# '):
        return 'heading', clean_text(line[2:])
    elif line.startswith('## '):
        return 'heading', clean_text(line[3:])
    
    # Subheadings (H3, H4)
    elif line.startswith('### '):
        return 'subheading', clean_text(line[4:])
    elif line.startswith('#### '):
        return 'subheading', clean_text(line[5:])
    
    # List items
    elif line.startswith('- '):
        return 'text', clean_text(line[2:])
    
    # Regular paragraphs
    else:
        cleaned = clean_text(line)
        # Only include substantial text (more than 3 characters)
        if len(cleaned) > 3:
            return 'text', cleaned
    
    return None, ""

def parse_markdown_to_json(markdown_path: str) -> List[Dict[str, str]]:
    """
    Parse markdown file and create structured JSON
    
    Args:
        markdown_path: Path to the markdown file
        
    Returns:
        List of dictionaries with 'type' and 'text' keys
    """
    
    print(f"📖 Reading markdown file: {markdown_path}")
    
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {markdown_path}")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []
    
    # Split into lines and process
    lines = content.split('\n')
    structured_content = []
    
    print(f"🔄 Processing {len(lines)} lines...")
    
    for line_num, line in enumerate(lines, 1):
        content_type, text = determine_content_type(line)
        
        if content_type and text:
            structured_content.append({
                'type': content_type,
                'text': text
            })
            
            # Show progress for important items
            if content_type in ['heading', 'subheading']:
                print(f"   Line {line_num:3d}: [{content_type.upper()}] {text[:60]}...")
    
    print(f"✅ Extracted {len(structured_content)} content items")
    return structured_content

def save_structured_json(content: List[Dict[str, str]], output_path: str):
    """Save structured content to JSON file"""
    try:
        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved structured JSON to: {output_path}")
        
        # Show file size
        file_size = Path(output_path).stat().st_size / 1024
        print(f"📊 Output file size: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")

def display_content_summary(content: List[Dict[str, str]], preview_count: int = 20):
    """Display summary and preview of parsed content"""
    
    # Count content types
    type_counts = {}
    for item in content:
        content_type = item['type']
        type_counts[content_type] = type_counts.get(content_type, 0) + 1
    
    print(f"\n📈 Content Statistics:")
    print(f"   Total items: {len(content)}")
    for content_type, count in sorted(type_counts.items()):
        print(f"   {content_type.capitalize()}: {count}")
    
    # Show preview
    print(f"\n📋 Content Preview (first {preview_count} items):")
    print("=" * 80)
    
    for i, item in enumerate(content[:preview_count]):
        content_type = item['type']
        text = item['text']
        
        # Truncate long text
        display_text = text[:100] + "..." if len(text) > 100 else text
        
        # Visual indicators
        if content_type == 'heading':
            print(f"{i+1:2d}. 🔴 [HEADING]")
        elif content_type == 'subheading':
            print(f"{i+1:2d}. 🟡 [SUBHEADING]")
        else:
            print(f"{i+1:2d}. 🔵 [TEXT]")
        
        print(f"    {display_text}")
        print()
    
    if len(content) > preview_count:
        print(f"... and {len(content) - preview_count} more items")
    
    print("=" * 80)

def main():
    """Main execution function"""
    
    # File paths
    input_markdown = "/Users/sauravtripathi/Downloads/auto-reel-video-gen/Sound-effects/test_pages_20-40.pdf.markdown"
    output_json = "/Users/sauravtripathi/Downloads/auto-reel-video-gen/Sound-effects/structured_content.json"
    
    print("🚀 Markdown to JSON Parser")
    print("=" * 50)
    
    # Check if input file exists
    if not Path(input_markdown).exists():
        print(f"❌ Input file not found: {input_markdown}")
        print("Please check the file path and try again.")
        return
    
    # Parse markdown to structured JSON
    structured_content = parse_markdown_to_json(input_markdown)
    
    if not structured_content:
        print("❌ No content was parsed from the markdown file.")
        return
    
    # Save structured JSON
    save_structured_json(structured_content, output_json)
    
    # Display summary and preview
    display_content_summary(structured_content)
    
    print(f"\n🎉 Success! Structured JSON created at:")
    print(f"   {output_json}")

# Utility functions for external use
def quick_parse(markdown_path: str, output_path: str = None) -> List[Dict[str, str]]:
    """
    Quick parsing function for external use
    
    Args:
        markdown_path: Path to markdown file
        output_path: Optional output path for JSON
        
    Returns:
        List of structured content dictionaries
    """
    content = parse_markdown_to_json(markdown_path)
    
    if output_path:
        save_structured_json(content, output_path)
    
    return content

if __name__ == "__main__":
    main()