# OUTPUT FOR THE TESTIMAGE 1.jpg and 2.jpg is:
# Time taken to execute first frame -> 0.057034034729003906 for first image 
# Time taken to execute after first frame -> 0.037034034729003906 takes little time as we are storing values for less calculation in future 
# Common Pixels -> 60353
# Total Pixels in Image -> 921600
# Difference in total pixels and common pixels is -> 861247

# Per Second We can send <=27 frames
# Now Next Problem after this will be we also need to see the network bandwidth and see how incoming and outgoing packets affects the limit of sending data over internet in that case for real time matching we have to send less frames skipping some frames which is another problem as both receiver and sender must align with same frame content to use this method but as we are working on ms for now we will have less error but still error is error LOL

import numpy as np
from PIL import Image
import time
import os
import cv2
import asyncio
import socket
import pickle
import threading

def camera_sleep():
    print("Camera operation start")
    time.sleep(0.100)  # Sleep for 5 milliseconds
    print("Camera operation end")

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

arr=[]
def load_image(file_path):
    img = Image.open(file_path).convert('RGB')
    return np.array(img, dtype=np.uint8)


async def send_array(array, writer):
    if not isinstance(array, np.ndarray):
        raise TypeError(f"Expected a NumPy array, but got {type(array)}.")
    # Serialize the NumPy array
    data = pickle.dumps(array)
    # Send the size of the serialized data first
    writer.write(len(data).to_bytes(4, byteorder='big'))
    await writer.drain()
    # Send the serialized data
    writer.write(data)
    await writer.drain()

async def send_data(data,cs):
    try:
        print(cs)
        UDP_IP = 'localhost'
        UDP_PORT = 12345
        CHUNK_SIZE = 480
        
            
        # Adjust the chunk size as needed to fit within typical MTU which supports 1500bytes but later we will use WebSockets so we can use upto 64KB
        # For right now i am setting 8000 as per index of array has 3bytes so we to qualize sender and reciever side chunksize i have made receiver_chunk=sender_chunk*3 we can increase but this is fine as we are getting <=27 frames which our camera normally captures it can be minimized for better performance as we are sending in our machine local host cant say about over the internet but as WebSockets has 64KB limit we can send more bytes as right now we are only using 8bytes=8000 and reciever side 24bytes=24000 so we can extend further but lets see what we can achieve we cant say for sure
        print(len(data[cs]))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            for i in range(0, len(data[cs]), CHUNK_SIZE):
                chunk = data[cs][i:i+CHUNK_SIZE]
                sock.sendto(chunk.tobytes(), (UDP_IP, UDP_PORT))
            empty_data=np.array([[0]],dtype=np.uint8)
            # print(empty_data)
            sock.sendto(empty_data.tobytes(), (UDP_IP, UDP_PORT))
        # print("Data sent successfully")
    except Exception as e:
        print(f"Error sending data: {e}")

maxcnt=1
# load and convert images to numpy arrays
# Since First Frame will be while connecting it can be sent without any optimization
async def main():
    global maxcnt
    reader, writer = await asyncio.open_connection('localhost', 5000)
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:

        ret, frame = cap.read()
        cnt=1
        if ret:
            # Store the captured frame in a variable
            captured_image = frame

            # Display the captured frame
            # cv2.imshow('Captured Image', captured_image)
            cv2.imwrite(str(cnt)+".jpg", frame)

            # Wait for 1 second (1000 milliseconds) before capturing the next frame
            # if cv2.waitKey(70) & 0xFF == ord('q'):  # Press 'q' to quit
            #     break    
        
        else:
            print("Error: Failed to capture frame.")

        index=0
        image1 = load_image(str(cnt)+".jpg")
        image1cpy = load_image(str(cnt)+".jpg")
        # array = array.astype(np.uint8)

        # Convert the numpy array to an image using PIL
        image = Image.fromarray(image1)

        # Save the image
        image.save('1.png')
        common_pixels_mask = np.all(image1 == image1cpy, axis=-1)
        common_pixels = image1[common_pixels_mask]
        coordinates = np.argwhere(common_pixels_mask)
        dtype = np.dtype([
                ('pixel_index', np.int32, (2,)),  # Two elements for the pixel index
                ('rgb', np.uint8, (3,))  # Three elements for the RGB values
            ])
        uncommon_pixels_array = np.zeros(coordinates.shape[0], dtype=dtype)
        uncommon_pixels_array['pixel_index'] = coordinates
        uncommon_pixels_array['rgb'] = common_pixels
        # print(common_pixels)
        # common_pixels_with_coordinates = np.concatenate((coordinates, common_pixels), axis=1)
        # print(common_pixels_with_coordinates)
        # arr.append(common_pixels_with_coordinates)
        # await send_data(arr,index)
        await send_array(uncommon_pixels_array,writer)
        # print(common_pixels_with_coordinates)
        # print(image1)


        index+=1
        cnt+=1

        # Our Optimization starts from here so I am mainly focusing on time taken for below part only
        start_t = time.time()
        # time.sleep(2)
        while True:
            maxcnt+=1
            camera_thread = threading.Thread(target=camera_sleep)
            camera_thread.start()
            ret, frame = cap.read()

            if ret:
                # Store the captured frame in a variable
                captured_image = frame

                # Display the captured frame
                # cv2.imshow('Captured Image', captured_image)
                cv2.imwrite(str(cnt)+".jpg", frame)
                # print(cnt)

                # Wait for 1 second (1000 milliseconds) before capturing the next frame
                # if cv2.waitKey(70) & 0xFF == ord('q'):  # Press 'q' to quit
                #     break    
        
            else:
                print("Error: Failed to capture frame.")


            image2 = load_image(str(cnt)+".jpg")
            cnt=2

            height, width, _ = image1.shape
            # print(height,width)
            scale_factor_y = 480 / 256
            scale_factor_x = 640 / 256

            # Using numpyarray comparison we find common pixels
            common_pixels_mask = np.all(image1 != image2, axis=-1)
            common_pixels = image1[common_pixels_mask]
            if(len(common_pixels)==0):
                continue
            coordinates = np.argwhere(common_pixels_mask)
            # original_coordinates = coordinates.astype(float)
            # original_coordinates[:, 0] = original_coordinates[:, 0] * scale_factor_y
            # original_coordinates[:, 1] = original_coordinates[:, 1] * scale_factor_x
            # original_coordinates = original_coordinates.astype(int)

            dtype = np.dtype([
                ('pixel_index', np.int32, (2,)),  # Two elements for the pixel index
                ('rgb', np.uint8, (3,))  # Three elements for the RGB values
            ])
            uncommon_pixels_array = np.zeros(coordinates.shape[0], dtype=dtype)
            uncommon_pixels_array['pixel_index'] = coordinates
            uncommon_pixels_array['rgb'] = common_pixels
            # common_pixels_with_coordinates = np.concatenate((coordinates, common_pixels), axis=1)
            # arr.append(common_pixels_with_coordinates)
            # await send_data(arr,index)
            await send_array(uncommon_pixels_array,writer)
            # print(common_pixels_with_coordinates.shape)


            index+=1
            # print(type(common_pixels))

            # Convert to a list if needed but since we will be using numpy in receiver end too so numpyarr will give us efficiency is replacing the pixels faster so we will send above numpyarr

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
                # print(f"{file_to_delete} has been deleted successfully.")
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
                # print(f"{current_file} has been renamed to {new_file}.")
            except FileNotFoundError:
                print(f"{current_file} does not exist.")
            except PermissionError:
                print(f"Permission denied to rename {current_file}.")
            except Exception as e:
                print(f"An error occurred while renaming the file: {e}")

            end_t = time.time()
            if end_t-start_t>=1:
                print(f"Time taken: {end_t - start_t}")
                start_t=time.time()
                print(maxcnt)
                maxcnt=0
            # print(f"Number of Common Pixels: {len(common_pixels)}")
            # print(f"Total Pixels: {height * width}")
            # print(f"Difference: {(height * width) - len(common_pixels)}")
                # break

            # Optional: Save common pixels if needed
            # np.savetxt('common_pixels.txt', common_pixels, fmt='%d')


if __name__ == "__main__":
    asyncio.run(main())
    # h=0
    # while True:
    #     h+=1