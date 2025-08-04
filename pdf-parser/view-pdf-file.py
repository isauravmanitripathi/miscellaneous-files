import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # pymupdf
from PIL import Image, ImageTk
import os
from io import BytesIO
from datetime import datetime

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer & Cropper")
        self.root.geometry("800x900")
        
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        
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
        ttk.Button(control_frame, text="Previous", command=self.prev_page).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Next", command=self.next_page).pack(side=tk.LEFT, padx=(0, 10))
        
        # Page info label
        self.page_label = ttk.Label(control_frame, text="No PDF loaded")
        self.page_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Zoom controls
        ttk.Label(control_frame, text="Zoom:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(control_frame, text="-", command=self.zoom_out).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(control_frame, text="+", command=self.zoom_in).pack(side=tk.LEFT, padx=(0, 10))
        
        # Crop status frame
        crop_frame = ttk.Frame(main_frame)
        crop_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Crop status label
        self.crop_status_label = ttk.Label(crop_frame, text="Press 'B' to start cropping, 'N' to finish", 
                                         foreground="blue", font=("Arial", 10, "bold"))
        self.crop_status_label.pack(side=tk.LEFT)
        
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
        
    def open_pdf(self):
        """Open and load a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
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
                
                # Update window title
                filename = os.path.basename(file_path)
                self.root.title(f"PDF Viewer & Cropper - {filename}")
                
                # Display first page
                self.display_page()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {str(e)}")
    
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
            
        # Save the cropped pages
        self.save_cropped_pdf()
        
    def save_cropped_pdf(self):
        """Save the selected pages as a new PDF"""
        try:
            # Create new PDF document
            new_pdf = fitz.open()
            
            # Copy selected pages
            for page_num in range(self.crop_start_page, self.crop_end_page + 1):
                new_pdf.insert_pdf(self.pdf_document, from_page=page_num, to_page=page_num)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.splitext(os.path.basename(self.root.title().split(" - ")[-1]))[0]
            output_filename = f"{original_name}_cropped_pages_{self.crop_start_page+1}_to_{self.crop_end_page+1}_{timestamp}.pdf"
            
            # Get the directory where the Python script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, output_filename)
            
            # Save the new PDF
            new_pdf.save(output_path)
            new_pdf.close()
            
            # Show success message
            messagebox.showinfo("Success", 
                              f"Cropped PDF saved successfully!\n\n"
                              f"Pages {self.crop_start_page+1} to {self.crop_end_page+1}\n"
                              f"Saved as: {output_filename}\n"
                              f"Location: {script_dir}")
            
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
            self.crop_status_label.config(text="Press 'B' to start cropping, 'N' to finish", 
                                        foreground="blue")
        else:
            self.crop_status_label.config(text=f"Cropping started at page {self.crop_start_page+1}. Navigate and press 'N' to finish.", 
                                        foreground="red")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.keysym == "Right" or event.keysym == "space":
            self.next_page()
        elif event.keysym == "Left":
            self.prev_page()
        elif event.keysym == "plus" or event.keysym == "equal":
            self.zoom_in()
        elif event.keysym == "minus":
            self.zoom_out()
        elif event.keysym.lower() == "b":
            self.start_crop()
        elif event.keysym.lower() == "n":
            self.finish_crop()

def main():
    # Ask for PDF path at startup
    root = tk.Tk()
    root.withdraw()  # Hide main window temporarily
    
    print("PDF Viewer & Cropper Starting...")
    file_path = filedialog.askopenfilename(
        title="Select PDF file to open",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected. Exiting...")
        return
    
    # Show main window and create viewer
    root.deiconify()
    viewer = PDFViewer(root)
    
    # Load the selected PDF
    try:
        viewer.pdf_document = fitz.open(file_path)
        viewer.total_pages = len(viewer.pdf_document)
        viewer.current_page = 0
        
        filename = os.path.basename(file_path)
        root.title(f"PDF Viewer & Cropper - {filename}")
        
        viewer.display_page()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open PDF: {str(e)}")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()