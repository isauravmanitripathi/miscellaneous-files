import sys
import json
import requests
import html2text
import re
from urllib.parse import urlparse, unquote

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py \"Article Name\" or python script.py \"https://en.wikipedia.org/wiki/Article_Name\"")
        sys.exit(1)
    
    input_str = sys.argv[1]
    try:
        fetch_and_save_wikipedia_article(input_str)
    except Exception as e:
        print(f"Error: {e}")