import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
import pyautogui

# Ensure Tesseract OCR path is set properly (adjust path for your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text Converter")
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.crop_box = None
        self.canvas = None
        self.screenshot = None
        self.tk_image = None

        # UI Elements
        self.text_area = tk.Text(root, height=10, width=60)
        self.text_area.pack(pady=10)

        self.capture_button = tk.Button(root, text="Capture Image (Snip Tool)", command=self.capture_image)
        self.capture_button.pack(pady=5)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

    def capture_image(self):
    
        self.root.withdraw()  
        self.screenshot = pyautogui.screenshot()
        self.root.deiconify()

        self.display_image(self.screenshot)

    def upload_image(self):
        
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            self.display_image(image)

    def display_image(self, image):
        
        top = tk.Toplevel(self.root)
        self.canvas = tk.Canvas(top, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        
        
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

       
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.image = image 

    def on_button_press(self, event):
       
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):

        end_x, end_y = (event.x, event.y)
        self.crop_box = (self.start_x, self.start_y, end_x, end_y)

        
        cropped_image = self.image.crop(self.crop_box)
        cropped_image.show()

        self.process_image(cropped_image)

    def process_image(self, image):
        # Text is extracted from image using Tesseract OCR
        text = pytesseract.image_to_string(image)
        self.display_text(text)

    def display_text(self, text):
        #extracted text is diaplayed
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToTextApp(root)
    root.mainloop()
