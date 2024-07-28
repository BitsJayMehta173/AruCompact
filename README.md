Efficient Video Meeting Application (Pre Frame Processing)

-------------------------------------

Main File :- sock.py(asynchronous server-client communication) , main.py , tkin.py , microservnp.py (nparrayloader)

sock.py(asynchronous server-client communication and nparray saver)

main.py (Algorithm Image Capture and Packet Sending)

microservnp.py (nparray decoder and image converser)

tkin.py (client application)

# https://www.youtube.com/watch?v=UY1NvGnDH3o  (YT-DEMO)

---------------------------------

## First run sock.py to estabish the server ->  run main.py -> wait for first packet send msg then run microservnp.py -> run tkin.py

Since the asynchronous server-client communication is not optimized we are getting lower frames but it will be faster with other packet sharing protocols but for now i am using this for demo purposes.

(As We need to create microservices for proper structure of camera with other services and threading, Main File will be updated later)
But I have implemented Camera function in same process for now for continuous flow and error handling
Now we are ready to send Data over internet but without any audio data.


Sender Side :- (main.py)[v6.0]
--------------------------------
Receiver Side :- (sock.py)[v6.0], (microservnp.py)[v6.0], (tkin.py)[v6.0]
--------------------------------

# LATEST UPDATES (V6.0)

I have finally completed a video transmission protype for local machine and it is processing 9-10 frames per second without quality decrease and it has been a serious achievement.
We are sending nparray in local machine for now but it consumes lots of space and sending it over the internet might also affect our space so we need to make a different data encoder for this like image index and rgb encoder in short we can make a small image which reflects the nparray with its values and as we are using uint32 for index we can also utilize it if we make this new nparray compressor which will use exactlu uint 8 type to store the index of pixels and rgb values


----------------------------------------------

# LATEST UPDATES (V5.0)

I have finally implemented a local machine prototype of my algorithm but due to low async I am getting poor results but using microservices and socket.io and sending over internet will be much faster.
It is Partnership Model of Video Application

--------------------------------
# LATEST UPDATES (V3.1)

I have used socket to transfer data in chunks to a local host server in my own machine for now.
We still have 1-2 sec latency due to chunks but as we will use WebSockets later on which Supports Upto 64KB chunk we can decrease the latency and quality is being processed as the original image was but we can later on try on decreasing quality for low network connectivity.

We need to Decode back the Recieved Data and reform the Image Frame by frame we will be using Tkinter to create a window which has Image component and updates image as we decode each frame one by one.

We have not added audio for now but we can create a separate microservice for it. As for now we are only focusing on Image transfer quality.

--------------------------------


--------------------------------
# LATEST UPDATES (V3.0)

I have made a rewrite feature which takes 2 simultaneous frames and deletes the first frame after each step and renames second frame as first frame and loops again

Frames Processed Per Second -> 31 

(IMPORTANT) Per Second We can send <=31 frames (if you dont move alot) But still it can decrease so Lets take average of 25frames

Now we have to send the numpy array of uncommon pixels over internet and process it in other end
So we need to create a receiver side processor which recieves the numpyarray and replaces pixels on the previous received image and keeps on doing until the receiving data is haulted or terminated.

--------------------------------
# LATEST UPDATES (V2.0)

OUTPUT FOR THE TESTIMAGE 1.jpg and 2.jpg is:

Time taken to execute first frame -> 0.057034034729003906 for first image 

Time taken to execute after first frame -> 0.037034034729003906 takes little time as we are storing values for less calculation in future 

Common Pixels -> 60353

Total Pixels in Image -> 921600

Difference in total pixels and common pixels is -> 861247

Fixed Time Consumption issue while comparison of common pixels using numpyarray

(IMPORTANT) Per Second We can send <=27 frames

Now Next Problem after this will be we also need to see the network bandwidth and see how incoming and outgoing packets affects the limit of sending data over internet in that case for real time matching we have to send less frames skipping some frames which is another problem as both receiver and sender must align with same frame content to use this method but as we are working on ms for now we will have less error but still error is error RIP😒🪦


---------------------------------
V-1.0 Result using normal array and for loops
OUTPUT FOR THE TESTIMAGE 1.jpg and 2.jpg is:

Time taken to execute first frame -> 0.9121508598327637 for first image 

Time taken to execute after first frame -> 0.5714099407196045 takes less time about half as we are storing values for less calculation in future 

Common Pixels -> 60353

Total Pixels in Image -> 921600

Difference in total pixels and common pixels is -> 861247

But further increasing each pixels into some effect mode suitable for ligthing according to the room and camera we can further increase the common pixels as we are missing many common pixels due to camera faults which can be covered with suitable effects

Since we are using normal For Loop and analysing each pixel one by one we have been facing time complexity but using numpyarray format can decrease the comparison time probably then found right now
(Solved in v2.0)using npmyarray

----------------------------------

basicflow.py contains the comparison and count of the common pixel of two frames

this is the basic how our image will be processed in the sender side which takes 0.5sec for each frame

so we have to work on only 2 frames per second and work accordingly to it

--------------------------

we will compare the pixels of two simultaneous frames captured from camera here and optimize the data to transfer

Using Dynamic Programming To Utilize the Time Complexity for unnecessary recalculations

we will scan two frames and take out the comparision and neglect the same pixels and replace the changed pixels,, if the rows of outer boundries are changing it can be neglected -- we will neglect it

we will take out the comparison between two frames
and also add the index in which the changes needs to be replaced
decreasing the amount of information being passed over the internet increases speed of transfer of data 
extra speciality can be used like adding hardcoded background like in Googlemeet and replace the background with custom background and now as you decreased the number of pixels in your frames the data needed to transfer has decreased to only the essential video frame parts
one more analysis is it can scan the face and recognises it well so whenever we remove our face from the cam it stops recognising and clears the background fully sending no data but only audio
as the side structures are important too and somewhat with similar characteristics it can know if it is same or not.
or a starting scan can be used to recognize only a single face and just represent it and this can be a silent mode picture where even when someone else enters your room the program will recognise only your face pixels as the owner and only send your images AKA Aru Silent Mode.
right now i am only working with video not the audio part and probably there might be no audio tranfer for now

to simulate the realtime face time in same machine we can decrease the quality and pixels size in the code itself which creates a efficient data streaming simulation too
and from next loop the start vector will reoccur with lower resolution
now after some time we will recheck the transmission (only for two machine interaction over internet)
and resume our better quality transfer

More Efficient Ideas are growing as of now

Primarily I was focusing on Video Editing features with less pixels storage but as the idea grew I went on to explore Video Chatting Application Coz Its Aru Time😂.

As The pixel quantity is decreased the RealTime Video Streaming or Chatting can be increased with upto same quality HD quality Video Calling Features as we can see in Meeting Space we dont have much movents which decreases the number of pixels to be changed over time and with the Background Hardcoding Neglation we are saving even more Data to transfer which makes a HD quality Video Chatting Even more possible.

But When there is movement we can see much disturbance in the RealTime Video Chatting which can be displayed with lowQuality Transfer by combining pixels into a avg. Pixel accordingly. 
I won't be using any specific protocols like Socket IO for now and just try to simulate the experience in same machine and try to optimize the Tranfer rate as much as possible.
