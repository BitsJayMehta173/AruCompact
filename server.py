import socket
import time
import sys
import numpy as np
import cv2
UDP_IP = "localhost"
UDP_PORT = 12345
CHUNK_SIZE = 24000  # The chuck_size keeping 24000 as each index has 3 values so Senderbyte Chunk_size*3 we are only using 24KB right now but we can use upto 64KB but due to camera restrictions we are only using 24KB

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
                    print(cnt)
                    start_t=time.time()
                if len(data) ==8:
                    cnt+=1
                    process_data(buffer)
                    buffer = b''  # Reset buffer for the next frame
                else:
                    buffer += data
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
        nparray = np.frombuffer(data, dtype=np.uint8)
        # reshape back to sent form for easy processing in future
        # nparray = nparray.reshape(-1, 3)
        # print(f"Processed NumPy array: {len(nparray)}")
        width, height = 640, 480  # Example dimensions

        # Create an empty image array
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        index = 0
        cnt=0
        for y in range(height):
            for x in range(width):
                if cnt>=len(nparray):
                    index=0
                    image_array[y, x] = nparray[index:index + 3]
                    continue
                image_array[y, x] = nparray[index:index + 3]
                index += 3
                cnt+=3
        
        image_filename = 'received_image.png'
        cv2.imwrite(image_filename, image_array)
        # print(f"Image saved as {image_filename}")
            
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    start_server()
    
