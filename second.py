import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import threading
import cv2
import time

cap = cv2.VideoCapture(0)

# for now we will loop 1.jpg and 2.jpg to make it like facetime

lastarr=[]
i=0

def starting(root):
    global lastarr
    # if i==0:
    #     image_path="1.jpg" 
    # else:
    #     image_path="2.jpg" 
    ret, frame = cap.read()

    if ret:
        # Convert the captured frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Store the frame as a NumPy array
        root.image_array = frame.astype(np.uint8)
    else:
        # If capturing fails, load a placeholder image
        root.image_array = np.array(Image.open("jp.jpeg"), dtype=np.uint8)

    image = Image.fromarray(root.image_array)
    root.tk_image = ImageTk.PhotoImage(image)
    lastarr = np.array(image, dtype=np.uint8)
    
    root.label = tk.Label(root, image=root.tk_image)
    root.label.pack()

    root.update_image_thread = threading.Thread(target=update_image, args=(root,))
    root.update_image_thread.daemon = True
    root.update_image_thread.start()

uparr=[]
def compare(current_image,last_image):
    # we will compare the pixels of two photos here and optimize the data to transfer
    global uparr,lastarr
    uparr=[]
    currarr = np.array(current_image, dtype=np.uint8)
    for i in range(currarr.shape[0]):
        for j in range(currarr.shape[1]):
            if np.array_equal(lastarr[i, j], currarr[i, j]):
                continue
            else:
                uparr.append((i, j, currarr[i, j]))
            lastarr[i,j]=currarr[i,j]

last_image=None

def update_image(root):
    global last_image
    if last_image==None:
        last_image = root.image_array.copy()
    while True:
        # image_path="jp.jpeg" #replace with newframe image from camera and pass it to change_pixels function to compare
        start_time = time.time()
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            current_image = frame.astype(np.uint8)

            compare(current_image, last_image)
            change_pixels(root, uparr)

            last_image = current_image
            root.tk_image = ImageTk.PhotoImage(Image.fromarray(root.image_array))
            root.label.config(image=root.tk_image)
            root.update_idletasks()
        end_time = time.time()
        print(end_time-start_time)
        

def change_pixels(root, indices):
    # we will scan two frames and take out the comparision and neglect the same pixels and replace the changed pixels if the rows of outer boundries are changing but can be neglected we will neglect it

    # root.image_array = np.array(root.last_image, dtype=np.uint8)
    # root.image_array = np.array(root.current_image, dtype=np.uint8)

    # we will take out the comparison from this np conversion and append in change_value array
    # and also add the index in which the changes need to be replaced
    # its same like when you open the meet and replace the background with custom meet background but infact it decreases the amount of information being passed over the internet and increases speed of transfer of data     

    # one more analysis is it scans the face and recognises it well so whenever we remove our face from the cam it stops recognising and clears the background
    # as the side structures are important too and somewhat with similar characteristics it can know if it is same or not.
    
    # or a starting scan can be used to recognize only a single face and just represent it and this can be a silent mode picture where even when someone else enters your room the program will recognise only your face pixels as the owner and only send your images.

    for index in indices:
        root.image_array[index[0], index[1]] = (index[2]+10).astype(np.uint8)

    # after changing we will store the current_image as last_image and clear current_image
    # to simulate the realtime face time we can decrease the quality and pixels size in the code itself which creates a efficient data streaming simulation too
    # we will use
    # start=time.now()
    # curr=time.now()-start
    # if curr>0.10:
        # quality=480
        # and from next loop the start vector will reoccur with lower resolution
        # now after some time we will recheck the transmission (only for internet)
        # and resume our better quality transfer
  
root = tk.Tk()

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    starting(root)
    root.mainloop()
