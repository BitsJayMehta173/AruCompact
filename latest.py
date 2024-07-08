# OUTPUT FOR THE TESTIMAGE 1.jpg and 2.jpg is:
# Time taken to execute first frame -> 0.057034034729003906 for first image 
# Time taken to execute after first frame -> 0.037034034729003906 takes little time as we are storing values for less calculation in future 
# Common Pixels -> 60353
# Total Pixels in Image -> 921600
# Difference in total pixels and common pixels is -> 861247

# Per Second We can send <=27 frames
# Now Next Problem after this will be we also need to see the network bandwidth and see how incoming and outgoing packets affects the limit of sending data over internet in that case for real time matching we have to send less frames skipping some frames which is another problem as both receiver and sender must align with same frame content to use this method but as we are working on ms for now we will have less error but still error is error LOL

# whenever we see very less number of common pixel we will be sending data continuously and instead of checking the common pixel we will check calmness after intervals of some second for efficiency

import numpy as np
from PIL import Image
import time
import os

def load_image(file_path):
    img = Image.open(file_path).convert('RGB')
    return np.array(img)

# load and convert images to numpy arrays
# Since First Frame will be while connecting it can be sent without any optimization
image1 = load_image('1.jpg')

# Our Optimization starts from here so I am mainly focusing on time taken for below part only
start_t = time.time()
image2 = load_image('2.jpg')

height, width, _ = image1.shape


# Using numpyarray comparison we find common pixels
common_pixels_mask = np.all(image1 == image2, axis=-1)

common_pixels = image1[common_pixels_mask]
print(common_pixels)

# Convert to a list if needed but since we will be using numpy in receiver end too so numpyarr will give us efficiency is replacing the pixels faster so we will send above numpyarr converting into list consumes lot of time as the frames have huge number of common pixels in ms simultaneous frames so it is better to avoid

# common_pixels_list = common_pixels.tolist()

# After completing the comparison and storing it into appropriate format we will send data over internet
# then we will copy the numpyarray of image2 in image1 numpyarray to avoid recalculations
# then we will delete lastframe and replace it with currentframe and since right now i am using demo data i am just storing two frame picture and deleting firstframe image after processing and renaming secondframe to firstframe name and capturing newframe and storing it as secondframe and loop goes on

image1=image2

current_directory = os.getcwd()
current_file="1.jpg"
file_to_delete = os.path.join(current_directory, current_file)

try:
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been deleted successfully.")
except FileNotFoundError:
    print(f"{file_to_delete} does not exist.")
except PermissionError:
    print(f"Permission denied to delete {file_to_delete}.")
except Exception as e:
    print(f"An error occurred while deleting the file: {e}")

# current_file="2.jpg"
current_file = os.path.join(current_directory, "2.jpg")
new_file = os.path.join(current_directory, "1.jpg")

try:
    os.rename(current_file, new_file)
    print(f"{current_file} has been renamed to {new_file}.")
except FileNotFoundError:
    print(f"{current_file} does not exist.")
except PermissionError:
    print(f"Permission denied to rename {current_file}.")
except Exception as e:
    print(f"An error occurred while renaming the file: {e}")

end_t = time.time()

print(f"Time taken: {end_t - start_t}")
print(f"Number of Common Pixels: {len(common_pixels)}")
print(f"Total Pixels: {height * width}")
print(f"Difference: {(height * width) - len(common_pixels)}")

# Optional: Save common pixels if needed
# np.savetxt('common_pixels.txt', common_pixels, fmt='%d')
