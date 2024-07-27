import cv2
import time

# Initialize the camera capture
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture frames continuously
    start=time.time()
    cnt=0
    while cnt<=26:
        # Capture a frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if ret:
            # Store the captured frame in a variable
            captured_image = frame

            # Display the captured frame
            # cv2.imshow('Captured Image', captured_image)
            cv2.imwrite(str(cnt)+".png", frame)

            # Wait for 1 second (1000 milliseconds) before capturing the next frame
            if cv2.waitKey(70) & 0xFF == ord('q'):  # Press 'q' to quit
                break
                
        else:
            print("Error: Failed to capture frame.")
        cnt+=1
    stop=time.time()
    print(stop-start)

    # Release the camera capture object
    cap.release()
    cv2.destroyAllWindows()

    print("Camera capture stopped.")

