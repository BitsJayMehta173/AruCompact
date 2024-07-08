import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import time
import threading

class ImageUpdater:
    def __init__(self, root, image_path):
        self.root = root
        self.image = Image.open(image_path)
        self.image_array = np.array(self.image, dtype=np.uint8)
        self.tk_image = ImageTk.PhotoImage(self.image)
        
        self.label = tk.Label(root, image=self.tk_image)
        self.label.pack()
        
        self.update_image_thread = threading.Thread(target=self.update_image)
        self.update_image_thread.daemon = True
        self.update_image_thread.start()
    
    def update_image(self):
        while True:
            # time.sleep(1)
            self.change_pixels()
            self.tk_image = ImageTk.PhotoImage(Image.fromarray(self.image_array))
            self.label.config(image=self.tk_image)
            self.root.update_idletasks()

    def change_pixels(self):
        # represent image array in uint8 type
        self.image_array = (self.image_array + [10, 0, 0]).astype(np.uint8)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUpdater(root, "jp.jpeg")
    root.mainloop()
