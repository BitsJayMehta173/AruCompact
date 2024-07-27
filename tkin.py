import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageUpdater:
    def __init__(self, root, image_path, update_interval=10, check_interval=5):
        self.root = root
        self.image_path = image_path
        self.update_interval = update_interval
        self.check_interval = check_interval

        self.label = tk.Label(root)
        self.label.pack()

        self.schedule_check()

    def schedule_check(self):
        # Schedule the file existence check
        self.root.after(self.check_interval, self.check_file)

    def check_file(self):
        if os.path.isfile(self.image_path):
            try:
                self.last_modified = os.path.getmtime(self.image_path)
                self.load_image()
                self.schedule_update()
            except Exception as e:
                print(f"Error checking file: {e}")
                self.schedule_check()  # Recheck after delay
        else:
            print(f"The file '{self.image_path}' does not exist. Checking again in {self.check_interval}ms.")
            self.schedule_check()  # Recheck after delay

    def schedule_update(self):
        # Schedule the image update
        self.root.after(self.update_interval, self.update_image)

    def update_image(self):
        try:
            if os.path.isfile(self.image_path):
                current_modified = os.path.getmtime(self.image_path)
                if current_modified != self.last_modified:
                    self.last_modified = current_modified
                    self.load_image()
                self.schedule_update()  # Schedule the next update
            else:
                print(f"The file '{self.image_path}' was deleted. Rechecking in {self.check_interval}ms.")
                self.schedule_check()  # Recheck after delay
        except Exception as e:
            print(f"Error updating image: {e}")
            self.schedule_check()  # Recheck after delay

    def load_image(self):
        try:
            # Load and display the image
            image = Image.open(self.image_path)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
        except Exception as e:
            print(f"Error loading image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    current_directory = os.getcwd()
    new_file = os.path.join(current_directory, "1.png")
    image_path = new_file  # Replace with your correct image path
    # image_path = "D:/Projects/AruCompact/1.jpg"  # Replace with your correct image path
    app = ImageUpdater(root, image_path)
    root.mainloop()


