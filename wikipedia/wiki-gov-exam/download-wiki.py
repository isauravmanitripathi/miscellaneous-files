import wikipedia
import html2text
import logging
import csv
import json
import os
from bs4 import BeautifulSoup
import re
import urllib.parse
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_wikipedia_html(html_content: str) -> str:
    """
    Cleans the HTML from a Wikipedia page by removing unwanted sections,
    links, and other elements before final conversion.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove [edit] links
    for edit_section in soup.find_all('span', class_='mw-editsection'):
        edit_section.decompose()

    # Remove "Main articles:", "See also:", etc. notes under headings
    for hatnote in soup.find_all('div', class_=re.compile(r'hatnote|seealso')):
        hatnote.decompose()
        
    # Remove the table of contents
    toc = soup.find('div', id='toc')
    if toc:
        toc.decompose()

    # Remove all citation links (e.g., [1], [2], etc.)
    for sup in soup.find_all('sup', class_='reference'):
        sup.decompose()

    # Remove image containers
    for thumb in soup.find_all('div', class_='thumb'):
        thumb.decompose()

    # Remove info boxes
    for infobox in soup.find_all('table', class_='infobox'):
        infobox.decompose()
        
    # Remove navigation boxes at the end
    for navbox in soup.find_all('div', class_='navbox'):
        navbox.decompose()

    return str(soup)

def extract_and_save_links(html_content: str, output_csv_filename: str):
    """
    Parses HTML content, extracts all hyperlinks, and saves them to a CSV file.
    """
    logging.info(f"Extracting links to save to {output_csv_filename}...")
    soup = BeautifulSoup(html_content, 'html.parser')
    links_data = []
    
    content_div = soup.find('div', class_='mw-parser-output')
    if not content_div:
        logging.warning("Could not find main content div ('mw-parser-output'). Links will not be extracted.")
        return

    for a_tag in content_div.find_all('a', href=True):
        href = a_tag.get('href', '')
        if href.startswith('/wiki/') and ':' not in href and not href.startswith('#'):
            link_text = a_tag.get_text(strip=True)
            full_url = 'https://en.wikipedia.org' + href
            if link_text:
                links_data.append({'text': link_text, 'url': full_url})

    if not links_data:
        logging.warning("No links found to extract.")
        return

    try:
        with open(output_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(links_data)
        logging.info(f"Successfully saved {len(links_data)} links to {output_csv_filename}")
    except IOError as e:
        logging.error(f"Could not write to CSV file: {e}")

def convert_markdown_to_json(markdown_content: str, chapter_name: str, output_json_filename: str):
    """
    Parses clean markdown content and converts it into a structured JSON file.
    """
    logging.info(f"Converting Markdown to JSON: {output_json_filename}...")
    lines = markdown_content.split('\n')
    
    preliminary_data = []
    current_section = None
    
    first_heading_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            first_heading_index = i
            break

    intro_content_lines = lines[:first_heading_index] if first_heading_index != -1 else lines
    body_lines = lines[first_heading_index:] if first_heading_index != -1 else []

    intro_text = "\n".join(intro_content_lines).strip()
    if intro_text:
        preliminary_data.append({
            "level": 1,
            "section_name": "Introduction",
            "generated_section_content_md": intro_text
        })

    for line in body_lines:
        heading_match = re.match(r'^(#+)\s+(.*)', line)
        if heading_match:
            if current_section:
                current_section["generated_section_content_md"] = current_section["generated_section_content_md"].strip()
                preliminary_data.append(current_section)
            
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            current_section = {
                "level": level,
                "section_name": heading_text,
                "generated_section_content_md": ""
            }
        elif current_section:
            current_section["generated_section_content_md"] += "\n" + line.strip()

    if current_section:
        current_section["generated_section_content_md"] = current_section["generated_section_content_md"].strip()
        preliminary_data.append(current_section)

    filtered_data = [s for s in preliminary_data if s["generated_section_content_md"]]
    
    final_json_data = []
    counters = [0] * 6

    for section in filtered_data:
        level = section["level"]
        
        if section["section_name"] == "Introduction":
            section_number = "1"
        else:
            counter_index = level - 2
            if 0 <= counter_index < len(counters):
                counters[counter_index] += 1
                for i in range(counter_index + 1, len(counters)):
                    counters[i] = 0
                
                section_number_parts = [str(c) for c in counters[:counter_index + 1]]
                section_number = ".".join(section_number_parts)
            else:
                section_number = "invalid_level"

        final_json_data.append({
            "chapter_name": chapter_name,
            "chapter_id": "1",
            "section_number": section_number,
            "section_name": section["section_name"],
            "generated_section_content_md": section["generated_section_content_md"]
        })

    try:
        with open(output_json_filename, 'w', encoding='utf-8') as f:
            json.dump(final_json_data, f, indent=4)
        logging.info(f"Successfully saved structured JSON data to {output_json_filename}")
    except IOError as e:
        logging.error(f"Could not write to JSON file: {e}")

def download_wikipedia_as_markdown(page_title: str, output_md_filename: str, output_csv_filename: str, output_json_filename: str) -> tuple[bool, str | None, str | None, str | None]:
    """
    Downloads, cleans, and processes a Wikipedia article.
    Returns (True, md_path, json_path, csv_path) on success.
    Returns (False, None, None, None) on failure.
    """
    try:
        logging.info(f"Searching for Wikipedia page: '{page_title}'")
        page = wikipedia.page(page_title, auto_suggest=False, redirect=True)
        html_content = page.html()
        logging.info("Successfully fetched the page content.")

        cleaned_html = clean_wikipedia_html(html_content)
        extract_and_save_links(cleaned_html, output_csv_filename)

        h = html2text.HTML2Text()
        h.ignore_links = True 
        h.ignore_images = True
        markdown_content = h.handle(cleaned_html)

        unwanted_headings = ['See also','Notes','References','Further reading','External links']
        pattern = re.compile(r'^(##\s*(' + '|'.join(unwanted_headings) + '))', re.MULTILINE | re.IGNORECASE)
        match = pattern.search(markdown_content)
        if match:
            markdown_content = markdown_content[:match.start()]
        
        markdown_content = markdown_content.strip()

        with open(output_md_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        convert_markdown_to_json(markdown_content, page.title, output_json_filename)

        print(f"✅ Article '{page.title}' processed successfully!")
        print(f"   ↪ Markdown saved to: {output_md_filename}")
        print(f"   ↪ Links CSV saved to: {output_csv_filename}")
        print(f"   ↪ JSON saved to: {output_json_filename}")
        return True, output_md_filename, output_json_filename, output_csv_filename

    except wikipedia.exceptions.PageError:
        logging.error(f"PageError: The page '{page_title}' does not exist on Wikipedia.")
        print(f"❌ Error: Could not find a Wikipedia page with the title '{page_title}'.")
        return False, None, None, None
    except wikipedia.exceptions.DisambiguationError as e:
        logging.error(f"DisambiguationError: '{page_title}' may refer to multiple pages.")
        print(f"❌ Error: '{page_title}' is a disambiguation page. Please be more specific. Options: {e.options}")
        return False, None, None, None
    except Exception as e:
        logging.error(f"An unexpected error occurred for page '{page_title}': {e}", exc_info=True)
        print(f"❌ An unexpected error occurred for '{page_title}': {e}")
        return False, None, None, None

def process_articles_from_csv(input_csv_path: str, url_column_name: str):
    """
    Reads a CSV file, processes each article, logs the status, and creates a new CSV with local paths.
    """
    if not os.path.exists(input_csv_path):
        print(f"❌ Error: The file '{input_csv_path}' was not found.")
        return

    # --- Setup for logging and new CSV ---
    log_filename = "processing_log.txt"
    output_csv_path = input_csv_path.rsplit('.', 1)[0] + "_processed.csv"
    updated_rows = []
    
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n--- Batch Process Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

    # --- Read all articles from the input CSV first ---
    articles_to_process = []
    original_fieldnames = []
    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if url_column_name not in reader.fieldnames:
                print(f"❌ Error: Column '{url_column_name}' not found in the CSV file.")
                print(f"   Available columns are: {', '.join(reader.fieldnames)}")
                return
            original_fieldnames = reader.fieldnames
            articles_to_process = list(reader)
            print(f"Found {len(articles_to_process)} articles to process...")

    except Exception as e:
        print(f"❌ Error: Could not read the CSV file. Please ensure it is a valid CSV. Details: {e}")
        return

    # --- Process each article ---
    success_count = 0
    failure_count = 0
    for i, row in enumerate(articles_to_process):
        url = row.get(url_column_name, "").strip()
        print(f"\n--- Processing article {i+1}/{len(articles_to_process)} ---")
        
        article_title = "Unknown"
        status = "FAILED"
        
        if not url or 'wikipedia.org/wiki/' not in url:
            print(f"⚠️  Skipping invalid Wikipedia URL: {url}")
            failure_count += 1
            reason = "Invalid or empty URL"
            md_path, json_path, links_csv_path = "N/A", "N/A", "N/A"
        else:
            try:
                article_title = urllib.parse.unquote(url.split('/wiki/')[-1])
                file_basename = article_title.lower().replace(' ', '_').replace('/', '_')

                md_folder, csv_folder, json_folder = "markdown", "csv", "json"
                os.makedirs(md_folder, exist_ok=True)
                os.makedirs(csv_folder, exist_ok=True)
                os.makedirs(json_folder, exist_ok=True)

                md_file = os.path.join(md_folder, f"{file_basename}.md")
                csv_file = os.path.join(csv_folder, f"{file_basename}_links.csv") 
                json_file = os.path.join(json_folder, f"{file_basename}.json")

                # Call the download function which now returns paths
                success, md_path_out, json_path_out, links_csv_path_out = download_wikipedia_as_markdown(article_title, md_file, csv_file, json_file)

                if success:
                    success_count += 1
                    status = "SUCCESS"
                    reason = "Downloaded successfully"
                    md_path, json_path, links_csv_path = md_path_out, json_path_out, links_csv_path_out
                else:
                    failure_count += 1
                    reason = "Failed during download/processing (see console for details)"
                    md_path, json_path, links_csv_path = "N/A", "N/A", "N/A"

            except Exception as e:
                print(f"❌ An unexpected critical error occurred for URL {url}: {e}")
                failure_count += 1
                reason = f"Critical error: {e}"
                md_path, json_path, links_csv_path = "N/A", "N/A", "N/A"
        
        # --- Update log file ---
        with open(log_filename, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{status}] Article: {article_title} | URL: {url} | Reason: {reason}\n")
        
        # --- Add new columns to the row data ---
        row['markdown_path'] = md_path
        row['json_path'] = json_path
        row['links_csv_path'] = links_csv_path
        updated_rows.append(row)

    # --- Write the new CSV file with the updated data ---
    new_fieldnames = original_fieldnames + ['markdown_path', 'json_path', 'links_csv_path']
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        print(f"\n✅ Successfully created updated CSV: {output_csv_path}")
    except IOError as e:
        print(f"\n❌ Error writing to output CSV file: {e}")

    print("\n--- Batch Processing Complete ---")
    print(f"✅ Successfully processed: {success_count} articles.")
    print(f"❌ Failed or skipped: {failure_count} articles.")
    print(f"ℹ️  A detailed log has been saved to: {log_filename}")
    print("-----------------------------------")


if __name__ == '__main__':
    # --- MODIFIED SECTION ---
    # The script no longer asks for input.
    # It uses the file 'dataset_final.csv' and assumes the URL column is named 'url'.
    
    print("--- Wikipedia Batch Downloader ---")
    
    # Define the input file path directly.
    # This assumes 'dataset_final.csv' is in the same folder as the script.
    input_csv_path = 'dataset_final.csv'
    
    # Define the column name that contains the Wikipedia URLs.
    # ** If your column name is different, change 'url' to the correct name here. **
    url_column = 'Economy Wikipedia Link'
    
    print(f"Reading from pre-configured file: '{input_csv_path}'")
    print(f"Using URL column: '{url_column}'")

    # Run the main processing function with the pre-configured settings.
    process_articles_from_csv(input_csv_path, url_column)
