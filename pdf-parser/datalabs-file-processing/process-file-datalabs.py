#!/usr/bin/env python3
"""
Datalab.to PDF Parser CLI Tool
Usage: 
  python pdf_parser.py <pdf_path> [options]          # Process single PDF
  python pdf_parser.py --folder <folder_path> [options]  # Process folder of PDFs
"""

import os
import sys
import time
import json
import base64
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv
import glob

# Load environment variables from .env file
load_dotenv()

class DatalabPDFParser:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.datalab.to/api/v1"
        self.headers = {"X-Api-Key": api_key}
    
    def parse_pdf(self, pdf_path, output_format="markdown", use_llm=False, 
                  force_ocr=False, save_images=True, output_dir=None):
        """
        Parse a PDF file using Datalab.to Marker API
        
        Args:
            pdf_path (str): Path to the PDF file
            output_format (str): Output format (markdown, html, json)
            use_llm (bool): Use LLM for enhanced accuracy
            force_ocr (bool): Force OCR on all pages
            save_images (bool): Save extracted images
            output_dir (str): Directory to save output files
        """
        
        # Validate PDF file
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        pdf_path = Path(pdf_path)
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError("File must be a PDF")
        
        print(f"📄 Processing PDF: {pdf_path.name}")
        print(f"🔧 Output format: {output_format}")
        print(f"🤖 Using LLM: {'Yes' if use_llm else 'No'}")
        print(f"👁️  Force OCR: {'Yes' if force_ocr else 'No'}")
        print("-" * 50)
        
        # Prepare form data
        with open(pdf_path, 'rb') as f:
            form_data = {
                'file': (pdf_path.name, f, 'application/pdf'),
                'output_format': (None, output_format),
                'use_llm': (None, use_llm),
                'force_ocr': (None, force_ocr),
                'format_lines': (None, True),  # Better formatting
                'disable_image_extraction': (None, not save_images)
            }
            
            # Submit request
            print("🚀 Submitting PDF to Datalab.to...")
            response = requests.post(
                f"{self.base_url}/marker", 
                files=form_data, 
                headers=self.headers
            )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        data = response.json()
        if not data.get('success'):
            raise Exception(f"API error: {data.get('error', 'Unknown error')}")
        
        request_id = data['request_id']
        check_url = data['request_check_url']
        
        print(f"✅ Request submitted successfully!")
        print(f"📋 Request ID: {request_id}")
        print("⏳ Waiting for processing to complete...")
        
        # Poll for results
        max_polls = 300  # 10 minutes max
        poll_interval = 2  # seconds
        
        for i in range(max_polls):
            time.sleep(poll_interval)
            
            response = requests.get(check_url, headers=self.headers)
            result = response.json()
            
            if result.get('status') == 'complete':
                print("🎉 Processing completed!")
                return self._save_results(result, pdf_path, output_dir, save_images)
            elif result.get('status') == 'error':
                raise Exception(f"Processing failed: {result.get('error', 'Unknown error')}")
            
            # Show progress
            if i % 15 == 0:  # Every 30 seconds
                print(f"⏳ Still processing... ({i*poll_interval}s elapsed)")
        
        raise Exception("Processing timed out after 10 minutes")
    
    def _save_results(self, result, pdf_path, output_dir, save_images):
        """Save the parsing results to files"""
        
        # Determine output directory
        if output_dir is None:
            output_dir = pdf_path.parent / f"{pdf_path.stem}_parsed"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        saved_files = []
        
        # Save main content
        output_format = result.get('output_format', 'markdown')
        if output_format in result:
            content = result[output_format]
            if content:
                file_ext = 'md' if output_format == 'markdown' else output_format
                output_file = output_dir / f"{pdf_path.stem}.{file_ext}"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    if output_format == 'json':
                        json.dump(content, f, indent=2, ensure_ascii=False)
                    else:
                        f.write(content)
                
                saved_files.append(output_file)
                print(f"💾 Saved {output_format}: {output_file}")
        
        # Save images
        images = result.get('images', {})
        if images and save_images:
            images_dir = output_dir / 'images'
            images_dir.mkdir(exist_ok=True)
            
            for img_name, img_base64 in images.items():
                try:
                    img_data = base64.b64decode(img_base64)
                    img_path = images_dir / img_name
                    
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    
                    saved_files.append(img_path)
                    print(f"🖼️  Saved image: {img_path}")
                except Exception as e:
                    print(f"⚠️  Failed to save image {img_name}: {e}")
        
        # Save metadata
        metadata = result.get('metadata', {})
        if metadata:
            metadata_file = output_dir / f"{pdf_path.stem}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            saved_files.append(metadata_file)
            print(f"📊 Saved metadata: {metadata_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("📋 PARSING SUMMARY")
        print("="*50)
        print(f"📄 Original PDF: {pdf_path}")
        print(f"📂 Output directory: {output_dir}")
        print(f"📄 Pages processed: {result.get('page_count', 'Unknown')}")
        print(f"💰 Total cost: ${result.get('total_cost', 0):.4f}")
        print(f"⏱️  Runtime: {result.get('runtime', 0):.2f}s")
        print(f"📁 Files saved: {len(saved_files)}")
        
        return {
            'output_dir': output_dir,
            'saved_files': saved_files,
            'result': result
        }

def find_pdf_files(folder_path):
    """Find all PDF files in the given folder"""
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    if not folder.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Find all PDF files (case insensitive)
    pdf_files = list(folder.glob("*.pdf")) + list(folder.glob("*.PDF"))
    
    # Remove duplicates and sort
    pdf_files = sorted(list(set(pdf_files)))
    
    return pdf_files

def ask_user_confirmation(pdf_path, current_index, total_count):
    """Ask user whether to process this PDF"""
    print(f"\n{'='*60}")
    print(f"📋 PDF {current_index}/{total_count}")
    print(f"📄 File: {pdf_path.name}")
    print(f"📂 Location: {pdf_path.parent}")
    print(f"📊 Size: {pdf_path.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"{'='*60}")
    
    while True:
        choice = input("\n🤔 Process this PDF? (y)es / (n)o / (s)kip all remaining / (q)uit: ").lower().strip()
        
        if choice in ['y', 'yes']:
            return 'process'
        elif choice in ['n', 'no']:
            return 'skip'
        elif choice in ['s', 'skip']:
            return 'skip_all'
        elif choice in ['q', 'quit']:
            return 'quit'
        else:
            print("❌ Invalid choice. Please enter 'y', 'n', 's', or 'q'")

def process_folder(parser_instance, folder_path, **kwargs):
    """Process all PDF files in a folder with user confirmation"""
    
    # Find all PDF files
    print(f"🔍 Scanning folder: {folder_path}")
    pdf_files = find_pdf_files(folder_path)
    
    if not pdf_files:
        print("❌ No PDF files found in the specified folder.")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF file(s)")
    
    # Process each PDF with user confirmation
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            # Ask user for confirmation
            user_choice = ask_user_confirmation(pdf_path, i, len(pdf_files))
            
            if user_choice == 'quit':
                print("\n👋 User requested to quit. Exiting...")
                break
            elif user_choice == 'skip_all':
                remaining = len(pdf_files) - i + 1
                print(f"\n⏭️  Skipping all remaining {remaining} PDF(s). Exiting...")
                skipped_count += remaining
                break
            elif user_choice == 'skip':
                print(f"⏭️  Skipping {pdf_path.name}")
                skipped_count += 1
                continue
            elif user_choice == 'process':
                print(f"\n🚀 Starting to process {pdf_path.name}...")
                
                # Process the PDF
                result = parser_instance.parse_pdf(
                    pdf_path=str(pdf_path),
                    **kwargs
                )
                
                processed_count += 1
                print(f"✅ Successfully processed: {pdf_path.name}")
                print(f"📂 Output saved to: {result['output_dir']}")
                
        except KeyboardInterrupt:
            print(f"\n❌ Process interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Failed to process {pdf_path.name}: {e}")
            failed_count += 1
            
            # Ask if user wants to continue after an error
            while True:
                continue_choice = input("\n🤔 Continue with next PDF? (y)es / (n)o: ").lower().strip()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("👋 Exiting...")
                    return
                else:
                    print("❌ Invalid choice. Please enter 'y' or 'n'")
    
    # Final summary
    print(f"\n{'='*60}")
    print("📊 BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"📄 Total PDFs found: {len(pdf_files)}")
    print(f"✅ Successfully processed: {processed_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(
        description="Parse PDF files using Datalab.to API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single PDF
  python pdf_parser.py document.pdf
  python pdf_parser.py document.pdf --format html --use-llm
  
  # Process folder of PDFs (with interactive confirmation)
  python pdf_parser.py --folder ./my_pdfs/
  python pdf_parser.py --folder /path/to/pdfs --use-llm --format json
        """
    )
    
    # Mutually exclusive group for single file vs folder
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('pdf_path', nargs='?', help='Path to a single PDF file to parse')
    input_group.add_argument('--folder', help='Path to folder containing PDF files to process')
    
    parser.add_argument('--api-key', 
                       default=os.environ.get('DATALABS_PDF_KEY'),
                       help='Datalab.to API key (or set DATALABS_PDF_KEY in .env file)')
    parser.add_argument('--format', 
                       choices=['markdown', 'html', 'json'], 
                       default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--use-llm', 
                       action='store_true',
                       help='Use LLM for enhanced accuracy (slower, costs more)')
    parser.add_argument('--force-ocr', 
                       action='store_true',
                       help='Force OCR on all pages (slower)')
    parser.add_argument('--no-images', 
                       action='store_true',
                       help='Skip image extraction')
    parser.add_argument('--output-dir',
                       help='Output directory (default: <pdf_name>_parsed for each PDF)')
    
    args = parser.parse_args()
    
    # Validate API key
    if not args.api_key:
        print("❌ Error: API key required!")
        print("Add DATALABS_PDF_KEY to your .env file or use --api-key option")
        print("\nTo set up .env file:")
        print("1. Create a .env file in the same directory as this script")
        print("2. Add: DATALABS_PDF_KEY=your-key-here")
        print("3. Or get an API key from https://www.datalab.to")
        sys.exit(1)
    
    try:
        # Initialize parser
        pdf_parser = DatalabPDFParser(args.api_key)
        
        # Common processing arguments
        process_kwargs = {
            'output_format': args.format,
            'use_llm': args.use_llm,
            'force_ocr': args.force_ocr,
            'save_images': not args.no_images,
            'output_dir': args.output_dir
        }
        
        if args.folder:
            # Process folder mode
            print("🗂️  FOLDER PROCESSING MODE")
            print("="*50)
            process_folder(pdf_parser, args.folder, **process_kwargs)
        else:
            # Process single file mode
            print("📄 SINGLE FILE PROCESSING MODE")
            print("="*50)
            result = pdf_parser.parse_pdf(pdf_path=args.pdf_path, **process_kwargs)
            print(f"\n🎉 Success! Check output in: {result['output_dir']}")
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()