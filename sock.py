import asyncio
import pickle
import numpy as np
from PIL import Image
import os


firsts=True

image_path = '1.png'
image = Image.open(image_path)
image_array = np.array(image)

def reshape_array(arr, group_size=9, target_shape=(480, 640)):
    total_elements = arr.size
    row_count, col_count = target_shape

    # Check if padding is needed
    padding = (group_size - (total_elements % group_size)) % group_size
    if padding != 0:
        arr = np.pad(arr, (0, padding), mode='constant')

    # Reshape the array into groups of 'group_size'
    grouped_array = arr.reshape(-1, group_size)

    # Flatten each group into a 1D array and reshape to the target shape
    reshaped_array = grouped_array.flatten()[:row_count * col_count].reshape(target_shape)
    
    return reshaped_array

async def handle_client(reader, writer):
    global firsts
    while True:
        # Receive the size of the serialized data
        data_size_bytes = await reader.read(4)
        if not data_size_bytes:
            print("Connection closed or no data received")
            return
        data_size = int.from_bytes(data_size_bytes, byteorder='big')
        data = b''
        while len(data) < data_size:
            packet = await reader.read(data_size - len(data))
            if not packet:
                print("Connection closed or error in receiving data")
                return
            data += packet
        # Deserialize the NumPy array
        try:
            array = pickle.loads(data)
            if isinstance(array, np.ndarray):
                # print("Received array with shape:", array.shape)
                # print("Received array dtype:", array.dtype)
                if firsts==True:
                    firsts=False
                    # print(array)
                    array1 = array[:, 2:]
                    # total_elements = 480 * 640
                    # array1 = np.arange(total_elements)
                    # reshaped_array = np.arange(total_elements)
                    # reshaped_array=reshape_array(array1)

                    # Reshape the array into shape (480, 640)
                    # array1 = array1.reshape((480, 640))
                    reshaped_array = array1.reshape((480, 640, 3))
                    # print(reshaped_array.shape)
                    image = Image.fromarray(reshaped_array)
                    image.save('1.png')
                else:
                    # os.remove('1.png')
                    # print(array)
                    # array1 = array[:, :2]
                    # print(array1)
                    for row in array:
                        x, y = row[0], row[1]
                        # print(x,y)
                        rgb = row[2:5]
                        # print(rgb)
                        image_array[x, y] = rgb
                    modified_image = Image.fromarray(image_array)
                    modified_image.save('2.png')
                    modified_image.save('1.png')

            else:
                print("Received object is not a NumPy array.")
                print("Type of received object:", type(array))
        except Exception as e:
            print("Deserialization error:", e)

async def receive_array(address=("localhost", 5000)):
    server = await asyncio.start_server(handle_client, *address)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(receive_array())
