import socket
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
UDP_IP = "localhost"
UDP_PORT = 12345
CHUNK_SIZE = 307200  # The chuck_size keeping 24000 as each index has 3 values so Senderbyte Chunk_size*3 we are only using 24KB right now but we can use upto 64KB but due to camera restrictions we are only using 24KB

# still we have lot of bytes left from 64KB so I guess we need to use it as we are only 50% back from the frame sent I think it might be synchronized with 1 sec latency as we have 27 frames in one second but still we need to improve for faster calling and if the speed is better we dont need to worry about quality as we are being sent the exact copy of image as captured by camera for now but we need to change it later making automatic quality decision for faster frame transfer

nparray=[]
cnt=1
flag=False
start_t=time.time()
def start_server():
    global cnt,flag,start_t
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((UDP_IP, UDP_PORT))
        print(f"Server listening on {UDP_IP}:{UDP_PORT}")
        buffer = b''  

        while True:
            try:

                # As the frames might not have 100% match from last frame it skips sending those pixels so as of now we are only receiving less than 8 frames which cannot be avoided as you cant go in future and send back those frames to optimize the efficiency but its same so per second we can see almost 5-8 as out of 27 frames cutting off common pixels we are getting upto 8-10 frames and there is little latency so we get little delay but if the image is not like video call we can add effects to make it realistic
                
                data, addr = server_socket.recvfrom(CHUNK_SIZE)
                # edge case when a frame is complete we receive a 8byte data we need to compress this but as of now I am using 8byte data as a flag
                # print(len(data))
                end_t=time.time()
                if flag==True and end_t-start_t>=1:
                    # print(cnt)
                    start_t=time.time()
                if len(data) ==1:
                    # print(len(data))
                    cnt+=1
                    process_data(buffer)
                    buffer = b''  # Reset buffer for the next frame
                else:
                    buffer += data
                    # temp = np.frombuffer(data, dtype=np.uint64).reshape(-1, 5)
                    # print(temp)
                    # break
                    flag=True
            except socket.error as e:
                print(f"Socket error: {e}")

def process_data(data):
    # function to process received data
    # We will create a async tkinter windows which updates its image component by processing the received data but before that we will need to convert our received data into a nparray and for that we will need to know about the frame so for todo list we will need to add a extra packet which will be empty packet which denotes frame change then we will combine the data but that might take alot of time so we need to asynchronously have to process the data as we recieve them. 

    # we might need to change the structure of server file to create a async structure for processing the data as we need to process received data in a specific way

    # start=time.time()
    # print(f"Received data length: {len(data)}")
    # print(sys.getsizeof(data))
    # right now we are getting data size as 24033 which is 24KB and WebSockets supports upto 64KB but lets see in future if we can achieve what we want but uptill now we are achieving what we wanted in our local machine cant say for over internet though
    # stop=time.time()
    # print(stop-start)

    #Decode received data assuming it's in bytes
    try:
        # Convert bytes back to a NumPy array
        print(len(data))
        nparray = np.frombuffer(data, dtype=np.uint8).reshape(-1, 5)
        print(nparray.shape)
        # reshape back to sent form for easy processing in future
        # coordinates = nparray[:, :2]
        # original_max_value
        # original_coordinates =(scaled_coordinates.astype(np.float32) / 255) * original_max_value
        
        rgbval = nparray[:, 2:]
        rgbval=rgbval.reshape(-1,640)
        # # print(coordinates)
        # # print(f"Processed NumPy array: {len(nparray)}")
        width, height =  480,640  # Example dimensions
        # scale_factor_y = 480 / 255
        # scale_factor_x = 640 / 255
        # original_coordinates = coordinates[:, :2].astype(np.float32)
        # original_coordinates[:, :2] *= scale_factor_y
        # original_coordinates[:, :2] *= scale_factor_x
        # original_coordinates = original_coordinates.astype(int)
        # common_pixels_with_coordinates = np.concatenate((original_coordinates, rgbval), axis=1)
        # print(common_pixels_with_coordinates)
        # Create an empty image array
        image_array = np.zeros((height, width, 3), dtype=np.uint8)
        # print(cnt)
        index = 0
        cnter=0
        if cnt==2:
            image = Image.fromarray(rgbval)

            # Save the image
            image.save('output_image.png')
            # Extract RGB values (last three columns)
            # rgb_values = image_array[:, -3:]

            # # Determine the shape of the image
            # # height = len(np.unique(image_array[:, 0]))  # unique y-coordinates
            # # width = len(np.unique(image_array[:, 1]))   # unique x-coordinates

            # # Create an empty image
            # image = np.zeros((700, 700, 3), dtype=np.uint8)
            # # scale_factor_y = 480 / 256
            # # scale_factor_x = 640 / 256

            # # Assign RGB values to the image

            # y=0
            # x=0
            # incx=0
            # incy=0
            # for row in nparray:
            #     # print(row)
            #     # temp=row[:2]
            #     # scaled_coordinates = row[:2]
            #     # print(scaled_coordinates)

            #     # # Height and width of the original image
            #     # height = 480.0
            #     # width = 640.0

            #     # # Convert back to original x coordinates
            #     # x = np.floor((scaled_coordinates[0].astype(np.float32) / 255) * width)

            #     # # Convert back to original y coordinates
            #     # y = np.floor((scaled_coordinates[1].astype(np.float32) / 255) * height)
            #     # x=x.astype(int)
            #     # y=y.astype(int)
            #     # y,x=row[:2]
            #     # print(x,y)
            #     # rgb = np.array(row[2:], dtype=np.uint8)
            #     # print(rgb)
            #     # # print(rgb)
            #     # if x+incx>=640:
            #     #     x=0
            #     # if y+incy>=480:
            #     #     y=0
                
            #     # print(x,y)
            #     image[y, x] = row[2:]
            #     x+=1
            #     if x==640:
            #         y+=1
            #         x=0

            # cv2.imwrite('output_image.jpg', image)
            
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    start_server()
    
