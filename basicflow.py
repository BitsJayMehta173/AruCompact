# OUTPUT FOR THE TESTIMAGE 1.jpg and 2.jpg is:
# Time taken to execute first frame - 0.9121508598327637 for first image 
# Time taken to execute after first frame - 0.5714099407196045 takes little time as we are storing values for less calculation in future 
# Common Pixels - 60353
# Total Pixels in Image - 921600
# Difference in total pixels and common pixels is - 861247

# we have saved network consumption by not sending 60353 pixels here and in each frame there will be some common pixels which we might not need to send as we already have last frame in receiver side and common pixel will be same while the changed pixels will be sent and replaced in reciever side
# but we still need to send 861237 pixels over internet

from PIL import Image
import os
import time

image1 = '1.jpg' 
img1 = Image.open(image1)
img1=img1.convert('RGB')
width, height = img1.size
arr=[]

for y in range(height):
    for x in range(width):
        arr.append(img1.getpixel((x, y)))
start_t=time.time()

image2 = '2.jpg' 

img2 = Image.open(image2)

# converting into RGB is faster as hardwares are more efficient while using RGB format and recognize RGB efficiently

img2=img2.convert('RGB')


cnt=0
c=0

# we are comparing two frames here to see how many pixels are common in two frames as if two frames have common pixel in same index then we can simple ignore sending those index pixels to send less data
i=0
for y in range(height):
    for x in range(width):
        temp=img2.getpixel((x, y))
        if arr[i]==temp:
            cnt+=1
        c+=1
        arr[i]=temp
        i+=1

end_t=time.time()
print(end_t-start_t)

print(cnt)
print(c)
