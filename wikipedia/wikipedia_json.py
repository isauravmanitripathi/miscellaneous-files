import sys
import json
import requests
import html2text
import re
from urllib.parse import urlparse, unquote

def parse_markdown_to_json(markdown_content):
    # Initialize the JSON structure
    json_structure = {}
    current_heading = None
    current_subheading = None
    current_content = [] # This will hold content for the current section (heading or subheading)
    current_table = None
    table_headers = None

    def add_content_to_structure(content_list):
        """Helper function to add accumulated content to the correct place in the JSON structure."""
        if not content_list:
            return

        # Flatten list of lists for content, but keep tables as dicts
        processed_content = []
        for item in content_list:
            if isinstance(item, list): # It's a list of list items
                if processed_content and isinstance(processed_content[-1], list):
                    processed_content[-1].extend(item) # Append to existing list if previous was also a list
                else:
                    processed_content.append(item)
            else: # It's a string (paragraph) or a dict (table)
                processed_content.append(item)

        if current_subheading and current_heading:
            if "content" not in json_structure[current_heading]["subheadings"][current_subheading]:
                json_structure[current_heading]["subheadings"][current_subheading]["content"] = []
            json_structure[current_heading]["subheadings"][current_subheading]["content"].extend(processed_content)
        elif current_heading:
            if "content" not in json_structure[current_heading]:
                json_structure[current_heading]["content"] = []
            json_structure[current_heading]["content"].extend(processed_content)
        # If there's no heading yet (content before the first heading), it will be ignored by this structure.
        # You might want to add a 'preamble' key if you expect content before the first # heading.

    # Split the Markdown content into lines
    lines = markdown_content.strip().split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            # If a blank line separates content, flush current_content
            if current_content:
                add_content_to_structure(current_content)
                current_content = []
            i += 1
            continue

        # Check for headings
        heading_match = re.match(r'^(#+)\s+(.+)$', line)
        if heading_match:
            # Before processing a new heading, save any accumulated content for the previous section
            if current_content:
                add_content_to_structure(current_content)
                current_content = []
            if current_table is not None: # Also save any pending table
                add_content_to_structure([{"table": current_table}])
                current_table = None
                table_headers = None

            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            if level == 1:
                current_heading = heading_text
                json_structure[current_heading] = {"content": [], "subheadings": {}}
                current_subheading = None # Reset subheading when a new top-level heading starts
            elif level >= 2 and current_heading:
                # Ensure the subheading dictionary exists
                if "subheadings" not in json_structure[current_heading]:
                    json_structure[current_heading]["subheadings"] = {}

                current_subheading = heading_text
                json_structure[current_heading]["subheadings"][current_subheading] = {"content": [], "subheadings": {}} # Allow deeper nesting for future if needed
            i += 1
            continue

        # Check for table start (lines starting with |)
        if line.startswith('|') and '|' in line[1:]:
            if current_content: # Flush any non-table content before starting a table
                add_content_to_structure(current_content)
                current_content = []

            if current_table is None:
                current_table = []
                # Assume the first line is headers
                table_headers = [header.strip() for header in line.split('|')[1:-1]]
                i += 1
                # Check for separator line (e.g., |---|---|) and skip it
                if i < len(lines) and re.match(r'^\|\s*-+\s*\|.*$', lines[i]):
                    i += 1
                continue
            # Parse table rows
            row_data = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(row_data) == len(table_headers):
                row_dict = dict(zip(table_headers, row_data))
                current_table.append(row_dict)
            i += 1
            continue
        # If not in a table, but previous table exists, save it
        elif current_table is not None:
            add_content_to_structure([{"table": current_table}])
            current_table = None
            table_headers = None

        # Check for list items
        list_match = re.match(r'^\s*[-*]\s+(.+)$', line)
        if list_match:
            # Start or continue a list
            # If the last item in current_content is already a list, append to it
            if current_content and isinstance(current_content[-1], list):
                current_content[-1].append(list_match.group(1).strip())
            else:
                current_content.append([list_match.group(1).strip()]) # Start a new list
            i += 1
            continue

        # Treat as paragraph or plain text
        # If we have a pending table, flush it before adding new paragraph content
        if current_table is not None:
            add_content_to_structure([{"table": current_table}])
            current_table = None
            table_headers = None

        current_content.append(line)
        i += 1

    # After the loop, save any remaining content or table
    if current_content:
        add_content_to_structure(current_content)
    if current_table is not None:
        add_content_to_structure([{"table": current_table}])

    return json_structure

def fetch_and_save_wikipedia_article(input_str):
    # Determine if input is URL or title
    if input_str.startswith('http://') or input_str.startswith('https://'):
        parsed_url = urlparse(input_str)
        path = parsed_url.path
        if path.startswith('/wiki/'):
            title = unquote(path[6:])
        else:
            raise ValueError("Invalid Wikipedia URL")
    else:
        title = input_str.replace(' ', '_')

    # Wikipedia API endpoint for parsed HTML
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "text",
        "formatversion": "2"
    }

    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()
    if 'error' in data:
        raise ValueError("Article not found or error: " + data['error']['info'])

    html_content = data['parse']['text']

    # Save HTML version
    html_filename = f"{title}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML article saved to {html_filename}")

    # Convert HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False  # Keep links
    h.ignore_images = False  # Keep images
    h.ignore_tables = False  # Keep tables
    markdown_content = h.handle(html_content)

    # Save original Markdown version
    md_filename = f"{title}.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"Markdown article saved to {md_filename}")

    # Clean Markdown: Remove all brackets, parentheses, and associated URLs/images
    # Remove flag images and other images, e.g., ![](//upload.wikimedia.org/.../40px-Flag_of_*.svg.png)
    cleaned_markdown = re.sub(r'!\[\]\(//upload\.wikimedia\.org/[^\)]*\)\s*', '', markdown_content)
    # Remove all content within square brackets and the brackets, e.g., [Text], [Text](...), [[edit](...)]
    cleaned_markdown = re.sub(r'\[([^\]]*)\]', '', cleaned_markdown)
    # Remove all content within parentheses and the parentheses, e.g., (Text), (/wiki/...)
    cleaned_markdown = re.sub(r'\([^)]*\)\s*', '', cleaned_markdown)

    # Save cleaned Markdown version
    cleaned_md_filename = f"{title}_cleaned.md"
    with open(cleaned_md_filename, 'w', encoding='utf-8') as f:
        f.write(cleaned_markdown)
    print(f"Cleaned Markdown article saved to {cleaned_md_filename}")

    # Parse cleaned Markdown to JSON
    json_structure = parse_markdown_to_json(cleaned_markdown)

    # Save JSON version
    json_filename = f"{title}_cleaned.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_structure, f, indent=2, ensure_ascii=False)
    print(f"JSON article saved to {json_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py \"Article Name\" or python script.py \"https://en.wikipedia.org/wiki/Article_Name\"")
        sys.exit(1)
    
    input_str = sys.argv[1]
    try:
        fetch_and_save_wikipedia_article(input_str)
    except Exception as e:
        print(f"Error: {e}")