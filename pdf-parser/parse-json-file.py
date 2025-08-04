#!/usr/bin/env python3
"""
PDF JSON Content Parser
Parse Datalab/Marker JSON output and extract content in reading order
"""

import json
import re
from typing import List, Dict, Any
from pathlib import Path

def clean_html_text(html_text: str) -> str:
    """Remove HTML tags and clean up text"""
    if not html_text:
        return ""
    
    # Remove HTML tags using regex
    clean_text = re.sub(r'<[^>]+>', '', html_text)
    
    # Replace HTML entities
    clean_text = clean_text.replace('&lt;', '<')
    clean_text = clean_text.replace('&gt;', '>')
    clean_text = clean_text.replace('&amp;', '&')
    clean_text = clean_text.replace('&quot;', '"')
    clean_text = clean_text.replace('&#x27;', "'")
    
    # Clean up whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text

def get_reading_order_position(bbox: List[float]) -> tuple:
    """
    Get position for sorting content in reading order (top to bottom, left to right)
    bbox format: [x1, y1, x2, y2]
    """
    if not bbox or len(bbox) < 4:
        return (0, 0)
    
    # Primary sort by y-coordinate (top to bottom)
    # Secondary sort by x-coordinate (left to right)
    y_pos = bbox[1]  # y1 coordinate
    x_pos = bbox[0]  # x1 coordinate
    
    return (y_pos, x_pos)

def extract_content_from_block(block: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract content from a single block"""
    content_items = []
    
    if not block or 'block_type' not in block:
        return content_items
    
    block_type = block['block_type']
    html_content = block.get('html', '')
    bbox = block.get('bbox', [])
    
    # Clean the text content
    text_content = clean_html_text(html_content)
    
    if not text_content.strip():
        return content_items
    
    # Determine the content type and extract text
    if block_type == 'SectionHeader':
        # Check the HTML to determine heading level
        if '<h1' in html_content:
            content_type = 'heading'
        elif '<h2' in html_content:
            content_type = 'heading'
        elif '<h3' in html_content:
            content_type = 'subheading'
        elif '<h4' in html_content:
            content_type = 'subheading'
        else:
            content_type = 'heading'  # Default for section headers
            
        content_items.append({
            'type': content_type,
            'text': text_content,
            'position': get_reading_order_position(bbox)
        })
    
    elif block_type == 'Text':
        content_items.append({
            'type': 'text',
            'text': text_content,
            'position': get_reading_order_position(bbox)
        })
    
    elif block_type == 'ListGroup':
        # Handle list groups - extract individual list items
        children = block.get('children', [])
        if children:
            for child in children:
                child_content = extract_content_from_block(child)
                content_items.extend(child_content)
        else:
            # Fallback: treat as text
            content_items.append({
                'type': 'text',
                'text': text_content,
                'position': get_reading_order_position(bbox)
            })
    
    elif block_type == 'ListItem':
        content_items.append({
            'type': 'text',
            'text': text_content,
            'position': get_reading_order_position(bbox)
        })
    
    elif block_type in ['PageHeader', 'PageFooter']:
        # Skip headers and footers
        pass
    
    else:
        # Handle other block types as text
        if text_content.strip():
            content_items.append({
                'type': 'text',
                'text': text_content,
                'position': get_reading_order_position(bbox)
            })
    
    return content_items

def parse_pdf_json(json_file_path: str) -> List[Dict[str, str]]:
    """Parse PDF JSON and extract content in reading order"""
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return []
    
    print(f"🔍 Analyzing JSON structure...")
    print(f"   Top-level type: {type(data)}")
    print(f"   Block type: {data.get('block_type', 'Unknown')}")
    
    all_content = []
    
    # Handle the document structure
    if isinstance(data, dict) and 'children' in data:
        pages = data['children']
        print(f"   Found {len(pages)} pages in document")
        
        # Process each page
        for page_idx, page in enumerate(pages):
            if not isinstance(page, dict):
                continue
                
            print(f"   Processing page {page_idx + 1}: {page.get('block_type', 'Unknown')}")
            
            # If this page has children, process them
            if 'children' in page and isinstance(page['children'], list):
                for block in page['children']:
                    content_items = extract_content_from_block(block)
                    all_content.extend(content_items)
            else:
                # Process the page itself as a block
                content_items = extract_content_from_block(page)
                all_content.extend(content_items)
    
    elif isinstance(data, list):
        # Handle list structure
        pages = data
        print(f"   Found {len(pages)} items in list structure")
        
        for page_idx, page in enumerate(pages):
            if isinstance(page, dict):
                print(f"   Processing item {page_idx + 1}: {page.get('block_type', 'Unknown')}")
                content_items = extract_content_from_block(page)
                all_content.extend(content_items)
    
    else:
        print(f"❌ Unexpected JSON structure: {type(data)}")
        return []
    
    print(f"📊 Extracted {len(all_content)} content items before sorting")
    
    # Sort content by reading order (top to bottom, left to right)
    all_content.sort(key=lambda x: x['position'])
    
    # Remove position info from final output and filter empty text
    final_content = []
    for item in all_content:
        if item['text'].strip():  # Only include non-empty text
            final_content.append({
                'type': item['type'],
                'text': item['text']
            })
    
    print(f"📊 Final content items: {len(final_content)}")
    return final_content

def save_parsed_content(content: List[Dict[str, str]], output_path: str):
    """Save parsed content to JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved parsed content to: {output_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def print_content_preview(content: List[Dict[str, str]], max_items: int = 10):
    """Print a preview of the parsed content"""
    print(f"\n📋 Content Preview (showing first {max_items} items):")
    print("=" * 60)
    
    for i, item in enumerate(content[:max_items]):
        content_type = item['type'].upper()
        text = item['text'][:100] + "..." if len(item['text']) > 100 else item['text']
        
        print(f"\n{i+1:2d}. [{content_type}]")
        print(f"    {text}")
    
    if len(content) > max_items:
        print(f"\n... and {len(content) - max_items} more items")

def main():
    """Main function"""
    
    # Configuration
    input_json_path = "/Users/sauravtripathi/Downloads/auto-reel-video-gen/Sound-effects/test_pages_20-40.pdf.json"
    output_json_path = "/Users/sauravtripathi/Downloads/auto-reel-video-gen/Sound-effects/parsed_content.json"
    
    print("🔄 PDF JSON Content Parser")
    print("=" * 50)
    
    # Check if input file exists
    if not Path(input_json_path).exists():
        print(f"❌ Input file not found: {input_json_path}")
        return
    
    print(f"📖 Reading: {input_json_path}")
    
    # Parse the JSON
    parsed_content = parse_pdf_json(input_json_path)
    
    if not parsed_content:
        print("❌ No content extracted!")
        return
    
    print(f"📊 Extracted {len(parsed_content)} content items")
    
    # Save parsed content
    save_parsed_content(parsed_content, output_json_path)
    
    # Show preview
    print_content_preview(parsed_content)
    
    # Show content type statistics
    type_counts = {}
    for item in parsed_content:
        content_type = item['type']
        type_counts[content_type] = type_counts.get(content_type, 0) + 1
    
    print(f"\n📈 Content Type Statistics:")
    for content_type, count in sorted(type_counts.items()):
        print(f"  {content_type}: {count}")

# Utility function for custom usage
def parse_custom_json(input_path: str, output_path: str = None):
    """
    Parse custom JSON file
    
    Usage:
        parse_custom_json("/path/to/input.json", "/path/to/output.json")
    """
    if output_path is None:
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_parsed.json"
    
    content = parse_pdf_json(input_path)
    save_parsed_content(content, output_path)
    return content

if __name__ == "__main__":
    main()