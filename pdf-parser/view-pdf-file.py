import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import fitz  # pymupdf
from PIL import Image, ImageTk
import os
import sys
from io import BytesIO
from datetime import datetime

class PDFViewer:
    def __init__(self, root, output_folder=None):
        self.root = root
        self.root.title("PDF Viewer & Cropper")
        self.root.geometry("800x900")
        
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        self.output_folder = output_folder
        self.pdf_filename = None
        
        # Cropping variables
        self.crop_start_page = None
        self.crop_end_page = None
        self.is_cropping = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Open PDF button
        ttk.Button(control_frame, text="Open PDF", command=self.open_pdf).pack(side=tk.LEFT, padx=(0, 10))
        
        # Navigation buttons
        ttk.Button(control_frame, text="Previous (1)", command=self.prev_page).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Next (2)", command=self.next_page).pack(side=tk.LEFT, padx=(0, 10))
        
        # Page info label
        self.page_label = ttk.Label(control_frame, text="No PDF loaded")
        self.page_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Zoom controls
        ttk.Label(control_frame, text="Zoom:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(control_frame, text="-", command=self.zoom_out).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(control_frame, text="+", command=self.zoom_in).pack(side=tk.LEFT, padx=(0, 10))
        
        # Output folder button
        ttk.Button(control_frame, text="Set Output Folder", command=self.set_output_folder).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Crop status frame
        crop_frame = ttk.Frame(main_frame)
        crop_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Crop status label
        self.crop_status_label = ttk.Label(crop_frame, text="Keys: 1=Previous, 2=Next, B=Start crop, N=Finish crop", 
                                         foreground="blue", font=("Arial", 10, "bold"))
        self.crop_status_label.pack(side=tk.LEFT)
        
        # Output folder info frame
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output folder label
        self.folder_label = ttk.Label(folder_frame, text=f"Output folder: {self.output_folder or 'Not set'}", 
                                    foreground="darkgreen", font=("Arial", 9))
        self.folder_label.pack(side=tk.LEFT)
        
        # Create scrollable frame for PDF display
        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse wheel for scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()  # Enable key bindings
        
    def set_output_folder(self):
        """Let user select output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder for Cropped PDFs")
        if folder:
            self.output_folder = folder
            self.folder_label.config(text=f"Output folder: {self.output_folder}")
        
    def open_pdf(self):
        """Open and load a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_pdf(file_path)
            
    def load_pdf(self, file_path):
        """Load a PDF file from given path"""
        try:
            # Close previous document if any
            if self.pdf_document:
                self.pdf_document.close()
            
            # Reset cropping variables
            self.crop_start_page = None
            self.crop_end_page = None
            self.is_cropping = False
            self.update_crop_status()
            
            # Open new PDF
            self.pdf_document = fitz.open(file_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            
            # Store filename for folder creation
            self.pdf_filename = os.path.splitext(os.path.basename(file_path))[0]
            
            # Update window title
            filename = os.path.basename(file_path)
            self.root.title(f"PDF Viewer & Cropper - {filename}")
            
            # Create output folder if not set
            if not self.output_folder:
                self.create_default_output_folder()
            
            # Display first page
            self.display_page()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF: {str(e)}")
    
    def create_default_output_folder(self):
        """Create default output folder based on PDF filename"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            folder_name = f"{self.pdf_filename}_cropped"
            self.output_folder = os.path.join(script_dir, folder_name)
            
            # Create folder if it doesn't exist
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
                
            self.folder_label.config(text=f"Output folder: {self.output_folder}")
            print(f"Created output folder: {self.output_folder}")
            
        except Exception as e:
            # Fallback to script directory
            self.output_folder = os.path.dirname(os.path.abspath(__file__))
            self.folder_label.config(text=f"Output folder: {self.output_folder} (fallback)")
            print(f"Warning: Could not create folder, using script directory: {e}")
    
    def display_page(self):
        """Display the current page"""
        if not self.pdf_document:
            return
            
        try:
            # Get the current page
            page = self.pdf_document[self.current_page]
            
            # Create transformation matrix for zoom
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            
            # Render page to image
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            # Convert to PIL Image and then to PhotoImage
            img = Image.open(BytesIO(img_data))
            self.photo = ImageTk.PhotoImage(img)
            
            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Add visual indicator if this page is marked for cropping
            if self.crop_start_page is not None and self.current_page == self.crop_start_page:
                # Add green border for start page
                self.canvas.create_rectangle(2, 2, img.width-2, img.height-2, 
                                           outline="green", width=4)
                self.canvas.create_text(10, 10, text="START", fill="green", 
                                      font=("Arial", 12, "bold"), anchor="nw")
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update page label
            page_text = f"Page {self.current_page + 1} of {self.total_pages}"
            if self.is_cropping:
                page_text += f" | Cropping: {self.crop_start_page + 1} to ?"
            self.page_label.config(text=page_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display page: {str(e)}")
    
    def next_page(self):
        """Go to next page"""
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page()
    
    def prev_page(self):
        """Go to previous page"""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page()
    
    def zoom_in(self):
        """Increase zoom level"""
        if self.pdf_document:
            self.zoom_level = min(self.zoom_level * 1.2, 5.0)  # Max zoom 5x
            self.display_page()
    
    def zoom_out(self):
        """Decrease zoom level"""
        if self.pdf_document:
            self.zoom_level = max(self.zoom_level / 1.2, 0.2)  # Min zoom 0.2x
            self.display_page()
    
    def start_crop(self):
        """Start cropping from current page"""
        if not self.pdf_document:
            messagebox.showwarning("Warning", "Please open a PDF first!")
            return
            
        self.crop_start_page = self.current_page
        self.crop_end_page = None
        self.is_cropping = True
        self.update_crop_status()
        self.display_page()  # Refresh to show visual indicator
        
    def finish_crop(self):
        """Finish cropping at current page and save"""
        if not self.is_cropping or self.crop_start_page is None:
            messagebox.showwarning("Warning", "Please start cropping first by pressing 'B'!")
            return
            
        self.crop_end_page = self.current_page
        
        if self.crop_end_page < self.crop_start_page:
            messagebox.showerror("Error", "End page must be after start page!")
            return
        
        # Ask user for filename
        self.ask_filename_and_save()
        
    def ask_filename_and_save(self):
        """Ask user for filename and save the cropped PDF"""
        # Generate default filename
        default_name = f"{self.pdf_filename}_pages_{self.crop_start_page+1}_to_{self.crop_end_page+1}"
        
        # Ask user for custom filename
        custom_name = simpledialog.askstring(
            "Save Cropped PDF",
            f"Enter filename for the cropped PDF:\n(Pages {self.crop_start_page+1} to {self.crop_end_page+1})\n\nWill be saved to:\n{self.output_folder}",
            initialvalue=default_name
        )
        
        if custom_name is None:  # User cancelled
            return
            
        if not custom_name.strip():  # Empty name
            messagebox.showwarning("Warning", "Please enter a valid filename!")
            return
            
        # Clean the filename (remove invalid characters)
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            custom_name = custom_name.replace(char, '_')
        
        # Add .pdf extension if not present
        if not custom_name.lower().endswith('.pdf'):
            custom_name += '.pdf'
            
        # Save the cropped PDF
        self.save_cropped_pdf(custom_name)
        
    def save_cropped_pdf(self, filename):
        """Save the selected pages as a new PDF with custom filename"""
        try:
            # Create new PDF document
            new_pdf = fitz.open()
            
            # Copy selected pages
            for page_num in range(self.crop_start_page, self.crop_end_page + 1):
                new_pdf.insert_pdf(self.pdf_document, from_page=page_num, to_page=page_num)
            
            # Use the set output folder
            output_path = os.path.join(self.output_folder, filename)
            
            # Check if file already exists
            if os.path.exists(output_path):
                response = messagebox.askyesno(
                    "File Exists", 
                    f"File '{filename}' already exists in the output folder. Do you want to overwrite it?"
                )
                if not response:
                    new_pdf.close()
                    return
            
            # Save the new PDF
            new_pdf.save(output_path)
            new_pdf.close()
            
            # Show success message
            messagebox.showinfo("Success", 
                              f"Cropped PDF saved successfully!\n\n"
                              f"Pages {self.crop_start_page+1} to {self.crop_end_page+1}\n"
                              f"Saved as: {filename}\n"
                              f"Location: {self.output_folder}")
            
            # Reset cropping variables
            self.crop_start_page = None
            self.crop_end_page = None
            self.is_cropping = False
            self.update_crop_status()
            self.display_page()  # Refresh display
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cropped PDF: {str(e)}")
    
    def update_crop_status(self):
        """Update the crop status label"""
        if not self.is_cropping:
            self.crop_status_label.config(text="Keys: 1=Previous, 2=Next, B=Start crop, N=Finish crop", 
                                        foreground="blue")
        else:
            self.crop_status_label.config(text=f"Cropping started at page {self.crop_start_page+1}. Use 1/2 to navigate, press 'N' to finish.", 
                                        foreground="red")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        # Navigation with number keys
        if event.keysym == "1":
            self.prev_page()
        elif event.keysym == "2":
            self.next_page()
        # Keep old navigation for compatibility
        elif event.keysym == "Right" or event.keysym == "space":
            self.next_page()
        elif event.keysym == "Left":
            self.prev_page()
        # Zoom controls
        elif event.keysym == "plus" or event.keysym == "equal":
            self.zoom_in()
        elif event.keysym == "minus":
            self.zoom_out()
        # Cropping controls
        elif event.keysym.lower() == "b":
            self.start_crop()
        elif event.keysym.lower() == "n":
            self.finish_crop()

def get_user_choice():
    """Ask user how they want to provide the PDF path"""
    print("PDF Viewer & Cropper")
    print("=" * 30)
    print("How would you like to provide the PDF file?")
    print("1. Type the file path in terminal")
    print("2. Browse and select file")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return int(choice)
        print("Please enter 1 or 2")

def get_pdf_path_from_terminal():
    """Get PDF path from user input"""
    while True:
        pdf_path = input("\nEnter the full path to your PDF file: ").strip().strip('"')
        
        if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
            return pdf_path
        elif os.path.exists(pdf_path):
            print("Error: File exists but is not a PDF file!")
        else:
            print("Error: File not found!")
        
        retry = input("Try again? (y/n): ").strip().lower()
        if retry != 'y':
            return None

def get_pdf_path_from_dialog():
    """Get PDF path using file dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    file_path = filedialog.askopenfilename(
        title="Select PDF file to open",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    root.destroy()
    return file_path if file_path else None

def get_output_folder():
    """Ask user for output folder"""
    print("\nOutput folder options:")
    print("1. Select a custom output folder")
    print("2. Auto-create folder (based on PDF name)")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            root = tk.Tk()
            root.withdraw()
            folder = filedialog.askdirectory(title="Select Output Folder for Cropped PDFs")
            root.destroy()
            return folder if folder else None
        elif choice == '2':
            return None  # Will auto-create
        print("Please enter 1 or 2")

def main():
    print("PDF Viewer & Cropper Starting...")
    
    # Get user choice for PDF input method
    choice = get_user_choice()
    
    # Get PDF path based on user choice
    if choice == 1:
        pdf_path = get_pdf_path_from_terminal()
    else:
        pdf_path = get_pdf_path_from_dialog()
    
    if not pdf_path:
        print("No PDF file selected. Exiting...")
        return
    
    # Get output folder choice
    output_folder = get_output_folder()
    
    # Create and start the GUI
    root = tk.Tk()
    viewer = PDFViewer(root, output_folder)
    
    # Load the selected PDF
    viewer.load_pdf(pdf_path)
    
    print(f"\nPDF loaded: {os.path.basename(pdf_path)}")
    print(f"Output folder: {viewer.output_folder}")
    print("\nGUI started. Use the application window for navigation and cropping.")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()