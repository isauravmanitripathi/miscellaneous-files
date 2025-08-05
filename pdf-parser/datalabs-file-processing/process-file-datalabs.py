#!/usr/bin/env python3
"""
Datalab.to PDF Parser CLI Tool
Usage: 
  python pdf_parser.py <pdf_path> [options]          # Process single PDF
  python pdf_parser.py --folder <folder_path> [options]  # Process folder of PDFs
  python pdf_parser.py --folder <folder_path> --auto [options]  # Process folder automatically
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
        
        # Print summary with safe formatting
        print("\n" + "="*50)
        print("📋 PARSING SUMMARY")
        print("="*50)
        print(f"📄 Original PDF: {pdf_path}")
        print(f"📂 Output directory: {output_dir}")
        
        # Safe formatting for potentially None values
        page_count = result.get('page_count')
        if page_count is not None:
            print(f"📄 Pages processed: {page_count}")
        else:
            print(f"📄 Pages processed: Unknown")
        
        total_cost = result.get('total_cost')
        if total_cost is not None:
            print(f"💰 Total cost: ${total_cost:.4f}")
        else:
            print(f"💰 Total cost: Not provided")
        
        runtime = result.get('runtime')
        if runtime is not None:
            print(f"⏱️  Runtime: {runtime:.2f}s")
        else:
            print(f"⏱️  Runtime: Not provided")
        
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

def is_already_processed(pdf_path):
    """Check if PDF has already been processed by looking for _parsed folder"""
    parsed_folder = pdf_path.parent / f"{pdf_path.stem}_parsed"
    return parsed_folder.exists() and parsed_folder.is_dir()

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

def ask_automatic_mode():
    """Ask user if they want to process all PDFs automatically"""
    print("\n🤖 PROCESSING MODE SELECTION")
    print("="*50)
    print("Choose processing mode:")
    print("1. ⚡ Automatic - Process all unprocessed PDFs without asking")
    print("2. 🎛️  Interactive - Ask for confirmation for each PDF")
    print("="*50)
    
    while True:
        choice = input("\nSelect mode (1 for automatic, 2 for interactive): ").strip()
        
        if choice == '1':
            return True  # Automatic mode
        elif choice == '2':
            return False  # Interactive mode
        else:
            print("❌ Invalid choice. Please enter '1' or '2'")

def process_folder(parser_instance, folder_path, auto_mode=False, **kwargs):
    """Process all PDF files in a folder with optional automatic mode"""
    
    # Find all PDF files
    print(f"🔍 Scanning folder: {folder_path}")
    pdf_files = find_pdf_files(folder_path)
    
    if not pdf_files:
        print("❌ No PDF files found in the specified folder.")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF file(s)")
    
    # Check which files are already processed
    unprocessed_files = []
    already_processed = []
    
    for pdf_path in pdf_files:
        if is_already_processed(pdf_path):
            already_processed.append(pdf_path)
        else:
            unprocessed_files.append(pdf_path)
    
    # Show processing status
    print(f"📊 Status: {len(unprocessed_files)} unprocessed, {len(already_processed)} already processed")
    
    if already_processed:
        print("\n📁 Already processed (skipping):")
        for pdf_path in already_processed:
            print(f"   ⏭️  {pdf_path.name}")
    
    if not unprocessed_files:
        print("\n🎉 All PDFs in this folder have already been processed!")
        return
    
    print(f"\n📋 Will process {len(unprocessed_files)} PDF(s)")
    
    # If not in auto mode from command line, ask user
    if not auto_mode:
        auto_mode = ask_automatic_mode()
    
    if auto_mode:
        print(f"\n⚡ AUTOMATIC MODE ENABLED")
        print(f"🚀 Processing {len(unprocessed_files)} unprocessed PDF(s) automatically...")
        print("="*60)
    
    # Process each unprocessed PDF
    processed_count = 0
    skipped_count = len(already_processed)  # Count already processed as skipped
    failed_count = 0
    
    # Keep track of skip_all state (only relevant in interactive mode)
    skip_all_remaining = False
    
    for i, pdf_path in enumerate(unprocessed_files, 1):
        try:
            if auto_mode:
                # Automatic mode - just process
                print(f"\n🚀 [{i}/{len(unprocessed_files)}] Processing: {pdf_path.name}")
                print("-" * 40)
                
                # Process the PDF
                result = parser_instance.parse_pdf(
                    pdf_path=str(pdf_path),
                    **kwargs
                )
                
                processed_count += 1
                print(f"✅ Successfully processed: {pdf_path.name}")
                print(f"📂 Output saved to: {result['output_dir']}")
                
            else:
                # Interactive mode - ask for confirmation
                
                # If user previously chose skip_all, don't ask again
                if skip_all_remaining:
                    print(f"⏭️  Skipping {pdf_path.name} (skip all remaining)")
                    skipped_count += 1
                    continue
                
                # Ask user for confirmation
                user_choice = ask_user_confirmation(pdf_path, i, len(unprocessed_files))
                
                if user_choice == 'quit':
                    print("\n👋 User requested to quit. Exiting...")
                    break
                elif user_choice == 'skip_all':
                    print(f"\n⏭️  Skipping {pdf_path.name} and all remaining PDFs...")
                    skip_all_remaining = True
                    skipped_count += 1
                    continue
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
                    
                    # After successful processing, continue to next PDF automatically
                    print(f"\n{'='*30}")
                    print("Moving to next PDF...")
                    print(f"{'='*30}")
                
        except KeyboardInterrupt:
            print(f"\n❌ Process interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Failed to process {pdf_path.name}: {e}")
            failed_count += 1
            
            if not auto_mode:
                # Ask if user wants to continue after an error (only in interactive mode)
                while True:
                    continue_choice = input("\n🤔 Continue with next PDF? (y)es / (n)o: ").lower().strip()
                    if continue_choice in ['y', 'yes']:
                        break
                    elif continue_choice in ['n', 'no']:
                        print("👋 Exiting...")
                        return
                    else:
                        print("❌ Invalid choice. Please enter 'y' or 'n'")
            else:
                # In automatic mode, just continue to next file
                print("⏭️  Continuing with next PDF...")
    
    # Final summary
    print(f"\n{'='*60}")
    print("📊 BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"📄 Total PDFs found: {len(pdf_files)}")
    print(f"✅ Successfully processed: {processed_count}")
    print(f"⏭️  Skipped (including already processed): {skipped_count}")
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
  
  # Process folder of PDFs (interactive mode)
  python pdf_parser.py --folder ./my_pdfs/
  python pdf_parser.py --folder /path/to/pdfs --use-llm --format json
  
  # Process folder of PDFs (automatic mode)  
  python pdf_parser.py --folder ./my_pdfs/ --auto
  python pdf_parser.py --folder /path/to/pdfs --auto --use-llm
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
    parser.add_argument('--auto',
                       action='store_true',
                       help='Automatically process all unprocessed PDFs without asking (folder mode only)')
    
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
    
    # Validate --auto flag usage
    if args.auto and not args.folder:
        print("❌ Error: --auto flag can only be used with --folder option")
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
            mode_text = "AUTOMATIC" if args.auto else "INTERACTIVE"
            print(f"🗂️  FOLDER PROCESSING MODE ({mode_text})")
            print("="*50)
            process_folder(pdf_parser, args.folder, auto_mode=args.auto, **process_kwargs)
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