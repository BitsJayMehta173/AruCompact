import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import threading
import cv2

# for now we will loop 1.jpg and 2.jpg to make it like facetime

cap = cv2.VideoCapture(0)

i=0

def starting(root):

    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
    # Capture a frame
        ret, frame = cap.read()

    # if i==0:
    #     image_path="1.jpg" 
    # else:
    #     image_path="2.jpg" 

    image_path="jp.jpeg" #replace with camera captured current image
    root.image = Image.open(image_path)
    root.image_array = np.array(root.image, dtype=np.uint8)
    root.tk_image = ImageTk.PhotoImage(root.image)
        
    root.label = tk.Label(root, image=root.tk_image)
    root.label.pack()

    root.update_image_thread = threading.Thread(target=update_image, args=(root,))
    root.update_image_thread.daemon = True
    root.update_image_thread.start()

uparr=[]

def compare(current_image,last_image):
    # we will compare the pixels of two photos here and optimize the data to transfer
    global uparr
    uparr=[]
    cnt=0
    currarr = np.array(current_image, dtype=np.uint8)
    lastarr = np.array(current_image, dtype=np.uint8) # we can store lastarr to avoid recalculating
    for i in range(currarr[0]):
        for j in range(currarr[1]):
            if lastarr[i][j][0]==currarr[i][j][0] and lastarr[i][j][1]==currarr[i][j][1] and lastarr[i][j][2]==currarr[i][j][2]:
                continue
            else:
                temp=[]
                temp.append(i)
                temp.append(j)
                temp.append(currarr[i][j])
                uparr.append(temp)
                cnt+=1
    print(cnt)


def update_image(root):
    while True:
        # image_path="jp.jpeg" #replace with newframe image from camera and pass it to change_pixels function to compare
        change_pixels(root)
        root.tk_image = ImageTk.PhotoImage(Image.fromarray(root.image_array))
        root.label.config(image=root.tk_image)
        root.update_idletasks()

def change_pixels(root, change_value, indices):
    # we will scan two frames and take out the comparision and neglect the same pixels and replace the changed pixels if the rows of outer boundries are changing but can be neglected we will neglect it

    # root.image_array = np.array(root.last_image, dtype=np.uint8)
    # root.image_array = np.array(root.current_image, dtype=np.uint8)

    # we will take out the comparison from this np conversion and append in change_value array
    # and also add the index in which the changes need to be replaced
    # its same like when you open the meet and replace the background with custom meet background but infact it decreases the amount of information being passed over the internet and increases speed of transfer of data     

    # one more analysis is it scans the face and recognises it well so whenever we remove our face from the cam it stops recognising and clears the background
    # as the side structures are important too and somewhat with similar characteristics it can know if it is same or not.
    
    # or a starting scan can be used to recognize only a single face and just represent it and this can be a silent mode picture where even when someone else enters your room the program will recognise only your face pixels as the owner and only send your images.

    change_value = [10, 0, 0]
    for index in indices:
        root.image_array[index] = (root.image_array[index] + change_value).astype(np.uint8)

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
starting(root)
image1 = '1.jpg' 
image2 = '2.jpg' 

root.mainloop()
