from marker.convert import convert_single_pdf
from marker.models import load_all_models
from marker.output import save_markdown_files
import json
import os

# Load models (done once; uses MPS on M2 if available, falls back to CPU)
model_lst = load_all_models()

# Provide your PDF path here
pdf_path = "path/to/your_book.pdf"  # Replace with your actual PDF file path

# Process the PDF (batch_multiplier=1 for low memory on M2)
full_text, images, out_meta = convert_single_pdf(pdf_path, model_lst, batch_multiplier=1)

# Prepare structured JSON output
# 'full_text' is a dict of pages with blocks; each block has 'block_type' (e.g., 'heading', 'text') 
# and 'section_hierarchy' (integer level: 1 for main heading, 2+ for subs, based on size/layout)
structured_data = {
    "metadata": out_meta,
    "pages": full_text,  # Hierarchical blocks per page
    "images": images  # If any, with descriptions
}

# Save to JSON
json_output_path = "output.json"
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(structured_data, f, indent=4, ensure_ascii=False)
print(f"JSON output saved to: {json_output_path}")

# Save to TXT (via Markdown conversion; headings as #/## based on levels)
md_output_dir = "output_md"
os.makedirs(md_output_dir, exist_ok=True)
md_filename = os.path.join(md_output_dir, os.path.basename(pdf_path).replace(".pdf", ""))
save_markdown_files(full_text, images, md_filename)

# Convert Markdown to plain TXT (strip # for headings if needed, but keeps structure)
txt_output_path = md_filename + ".txt"
with open(md_filename + ".md", "r", encoding="utf-8") as md_file:
    md_content = md_file.read()
with open(txt_output_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(md_content)  # Or process further to flatten if desired
print(f"TXT output saved to: {txt_output_path}")