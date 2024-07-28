import numpy as np
from PIL import Image
import time
import os


start_t = time.time()

while True:
    try:
        if os.path.exists('array.npy'):
            uncommon_pixels_array = np.load('array.npy')

            if os.path.exists('1.png'):
                reconstructed_image_pil = Image.open('1.png')
                reconstructed_image = np.array(reconstructed_image_pil)
            else:
                reconstructed_image = np.zeros((480, 640, 3), dtype=np.uint8)

            pixel_indices = uncommon_pixels_array['pixel_index']
            rgb_values = uncommon_pixels_array['rgb']

            reconstructed_image[pixel_indices[:, 0], pixel_indices[:, 1]] = rgb_values

            reconstructed_image_pil = Image.fromarray(reconstructed_image)

            reconstructed_image_pil.save('1.png')

            end_t = time.time()
            print(f"Elapsed time: {end_t - start_t:.2f} seconds")

        else:
            print("array.npy file not found. Waiting for the file...")

        

    except Exception as e:
        print(f"An error occurred: {e}")

        
