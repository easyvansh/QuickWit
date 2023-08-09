import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import fitz  # PyMuPDF
from PIL import Image, ImageTk

class PDFSpeedReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Speed Reader")
        
        # Convert PNG icon to ICO format
        icon_image = Image.open("assets/quick_wit_icon.png")
        self.icon = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(True, self.icon)

        self.pdf_path = ""
        self.words = []
        self.word_index = 0
        self.speed = 300  # Default speed: Words per minute
        self.paused = False
        
        # Style for themed widgets
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.map("TButton", background=[('active', '!disabled', 'lightblue')])
        
        # Text display label
        self.text_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.text_label.pack(padx=20, pady=20)
        
        # Start button to begin reading
        self.start_button = ttk.Button(root, text="Start", command=self.start_reading)
        self.start_button.pack(pady=10)
        
        # Stop button to pause reading
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_reading)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)
        
        # Resume button to resume reading after stopping
        self.resume_button = ttk.Button(root, text="Resume", command=self.resume_reading)
        self.resume_button.pack(pady=10)
        self.resume_button.config(state=tk.DISABLED)

        # Previous button to go back reading after stopping
        self.previous_button = ttk.Button(root, text="Previous", command=self.previous_reading)
        self.previous_button.pack(pady=10)
        self.previous_button.config(state=tk.DISABLED)

        # Next button to go next reading after stopping
        self.next_button = ttk.Button(root, text="Next", command=self.next_reading)
        self.next_button.pack(pady=10)
        self.next_button.config(state=tk.DISABLED)
        
        # Load PDF button
        self.load_pdf_button = ttk.Button(root, text="Load PDF", command=self.load_pdf)
        self.load_pdf_button.pack(pady=10)
        
        # Speed control (WPM)
        self.speed_label = ttk.Label(root, text="Speed (WPM):")
        self.speed_label.pack()
        
        # Label to display the current WPM value
        self.wpm_label = ttk.Label(root, text=f"{self.speed} WPM")
        self.wpm_label.pack()
        
        self.speed_scale = ttk.Scale(root, from_=100, to=600, orient=tk.HORIZONTAL, length=300, command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()
        
        
    def load_pdf(self):
        """Load a PDF file using the file dialog."""
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.words = self.extract_text_from_pdf()
            self.word_index = 0
        
    def extract_text_from_pdf(self):
        """Extract text from a PDF file using PyMuPDF."""
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.split()
    
    def stop_reading(self):
        """Pause the reading process."""
        self.paused = True
        self.stop_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        self.previous_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        
    def resume_reading(self):
        """Resume the reading process."""
        self.paused = False
        self.resume_button.config(state=tk.DISABLED)
        self.start_reading()

    def previous_reading(self):
        """Resume the reading process."""
        self.paused = True
        self.previous_button.config(state=tk.NORMAL)
        word = self.words[self.word_index]
        self.text_label.config(text=word)
        self.word_index -= 1
        
        # Ensure non-zero speed
        delay = 60.0 / (self.speed + 1e-6)
        
        # Update the GUI
        self.root.update()

    def next_reading(self):
        """Resume the reading process."""
        self.paused = True
        self.next_button.config(state=tk.NORMAL)
        word = self.words[self.word_index]
        self.text_label.config(text=word)
        self.word_index += 1
        
        # Ensure non-zero speed
        delay = 60.0 / (self.speed + 1e-6)
        
        # Update the GUI
        self.root.update()
        
        
    def start_reading(self):
        """Start the reading process."""
        if not self.pdf_path:
            messagebox.showerror("Error", "Please load a PDF first.")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.load_pdf_button.config(state=tk.DISABLED)
        self.speed_scale.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)  # Enable Stop button
        self.resume_button.config(state=tk.DISABLED)  # Disable Resume button
        
        while self.word_index < len(self.words) and not self.paused:
            word = self.words[self.word_index]
            self.text_label.config(text=word)
            
            self.word_index += 1
            
            # Ensure non-zero speed
            delay = 60.0 / (self.speed + 1e-6)
            
            # Update the GUI
            self.root.update()
            
            if self.word_index == len(self.words) - 1:
                delay *= 3  # Display the last word for a longer time
                
            time.sleep(delay)
            
        if self.word_index == len(self.words):
            self.text_label.config(text="Reading Complete")
        
        self.start_button.config(state=tk.NORMAL)
        self.load_pdf_button.config(state=tk.NORMAL)
        self.speed_scale.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)  # Disable Stop button
        self.resume_button.config(state=tk.NORMAL)  # Enable Resume button
        
    def update_speed(self, value):
        """Update the reading speed (WPM) and display the current WPM value."""
        self.speed = int(float(value))
        self.wpm_label.config(text=f"{self.speed} WPM")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSpeedReaderApp(root)
    root.mainloop()
