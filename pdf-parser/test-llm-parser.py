#!/usr/bin/env python3
"""
PDF Page Range Extractor
Extract specific pages from a PDF and save as a new PDF file
"""

import PyPDF2
import os
from pathlib import Path

def extract_pdf_pages(input_pdf_path, start_page, end_page, output_pdf_path=None):
    """
    Extract specific pages from a PDF and save as new PDF
    
    Args:
        input_pdf_path (str): Path to input PDF file
        start_page (int): Starting page number (1-based)
        end_page (int): Ending page number (1-based, inclusive)
        output_pdf_path (str, optional): Path for output PDF. If None, auto-generates name
    
    Returns:
        str: Path to the created PDF file, or None if failed
    """
    
    try:
        # Validate input file exists
        if not os.path.exists(input_pdf_path):
            print(f"❌ Error: Input file '{input_pdf_path}' not found!")
            return None
        
        print(f"📖 Opening PDF: {os.path.basename(input_pdf_path)}")
        
        # Open the PDF file
        with open(input_pdf_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            total_pages = len(pdf_reader.pages)
            
            print(f"📄 Total pages in PDF: {total_pages}")
            
            # Validate page range
            if start_page < 1:
                print("❌ Error: Start page must be 1 or greater")
                return None
            
            if end_page > total_pages:
                print(f"❌ Error: End page ({end_page}) exceeds total pages ({total_pages})")
                return None
            
            if start_page > end_page:
                print("❌ Error: Start page cannot be greater than end page")
                return None
            
            print(f"✂️  Extracting pages {start_page} to {end_page} ({end_page - start_page + 1} pages)")
            
            # Create PDF writer
            pdf_writer = PyPDF2.PdfWriter()
            
            # Extract pages (convert to 0-based indexing)
            pages_extracted = 0
            for page_num in range(start_page - 1, end_page):
                try:
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
                    pages_extracted += 1
                    print(f"  ✅ Added page {page_num + 1}")
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not extract page {page_num + 1}: {e}")
            
            # Generate output filename if not provided
            if output_pdf_path is None:
                input_path = Path(input_pdf_path)
                output_pdf_path = input_path.parent / f"{input_path.stem}_pages_{start_page}-{end_page}.pdf"
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_pdf_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Write the new PDF
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"💾 Successfully saved {pages_extracted} pages to: {output_pdf_path}")
            
            # Show file size
            file_size = os.path.getsize(output_pdf_path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"📊 Output file size: {file_size_mb:.2f} MB")
            
            return str(output_pdf_path)
    
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{input_pdf_path}'")
        return None
    except Exception as e:
        print(f"❌ Error processing PDF: {str(e)}")
        return None

def main():
    """Main function with your specific file path"""
    
    # Your file configuration
    input_pdf = "/Users/sauravtripathi/Desktop/pdfs/test.pdf"
    start_page = 224
    end_page = 228
    output_pdf = "/Users/sauravtripathi/Desktop/pdfs/test_pages_20-40.pdf"
    
    print("🔄 PDF Page Extractor")
    print("=" * 50)
    
    # Extract the pages
    result = extract_pdf_pages(input_pdf, start_page, end_page, output_pdf)
    
    if result:
        print("\n✅ SUCCESS!")
        print(f"📁 Original file: {input_pdf}")
        print(f"📁 New file: {result}")
        print(f"📄 Pages extracted: {start_page}-{end_page}")
        
        # Show original vs new file sizes
        try:
            original_size = os.path.getsize(input_pdf) / (1024 * 1024)
            new_size = os.path.getsize(result) / (1024 * 1024)
            print(f"📊 Size reduction: {original_size:.2f} MB → {new_size:.2f} MB")
        except:
            pass
    else:
        print("\n❌ FAILED!")
        print("Please check the error messages above.")

# Utility function for custom usage
def extract_pages_custom(pdf_path, start, end, output_path=None):
    """
    Simple function for custom page extraction
    
    Usage:
        extract_pages_custom("/path/to/file.pdf", 20, 40, "/path/to/output.pdf")
    """
    return extract_pdf_pages(pdf_path, start, end, output_path)

if __name__ == "__main__":
    main()