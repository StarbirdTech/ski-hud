import cv2
import json
from lib import serialSelect

# load serial port

vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print("Cannot open camera")
    exit()

frameW = int(vid.get(3))
frameH = int(vid.get(4))
frameRatio = frameW / frameH

screenW = 128
screenH = 64
screenRatio = screenW / screenH

while (True):
    ret, frame = vid.read()

    if ret == True:
        if frameRatio == screenRatio:
            frame = frame[0:screenW, 0:screenH]
        elif frameRatio > screenRatio:
            frame = frame[0:frameH, int((frameW - (frameH * screenRatio)) / 2):int((frameW + (frameH * screenRatio)) / 2)]
        else:
            frame = frame[int((frameH - (frameW / screenRatio)) / 2):int((frameH + (frameW / screenRatio)) / 2), 0:frameW]

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Enhance the contrast and reduce the noise
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        gray = cv2.medianBlur(gray, 5)

        # Apply Otsu's thresholding to segment the objects
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Apply morphological opening to remove small objects
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Detect contours of the objects
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through each contour
        for cnt in contours:
            # Filter out small or spurious contours
            if cv2.contourArea(cnt) < 25:
                continue

            # Check if the contour is touching the bottom of the frame
            x, y, w, h = cv2.boundingRect(cnt)
            if y + h == frame.shape[0]:
                continue

            # Compute the center position
            M = cv2.moments(cnt)
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])

            objects = []
            objects.append((center_x, center_y))

        largeFrame = frame

        # Get the height and width of the image
        height, width = largeFrame.shape[:2]
        
        # Define the points from which the images will be cropped
        top_left = (0, 0)  # (x, y)
        bottom_right = (width, height)  # (x, y)
        
        # Define the size of each cropped image
        crop_top_left_size = (128, 64)  # (width, height)
        crop_bottom_right_size = (int(width/2), int(height/2))  # (width, height)
        
        # Crop the image into two smaller images
        leftFrame = largeFrame[top_left[1]:top_left[1]+crop_top_left_size[1], top_left[0]:top_left[0]+crop_top_left_size[0]]
        rightFrame = largeFrame[bottom_right[1]-crop_bottom_right_size[1]:bottom_right[1], bottom_right[0]-crop_bottom_right_size[0]:bottom_right[0]]
        
        # map object coordinates to cropped frames and set to leftObjects and rightObjects
        leftObjects = []
        rightObjects = []
        for i in range(len(objects)):
            if objects[i][0] < crop_top_left_size[0] and objects[i][1] < crop_top_left_size[1]:
                leftObjects.append((objects[i][0], objects[i][1]))
            elif objects[i][0] > crop_top_left_size[0] and objects[i][1] > crop_top_left_size[1]:
                rightObjects.append((objects[i][0] - crop_top_left_size[0], objects[i][1] - crop_top_left_size[1]))

        for i in range(len(objects)):
            cv2.circle(largeFrame, (objects[i][0], objects[i][1]), 5, (0, 0, 255), -1)
        for i in range(len(leftObjects)):
            cv2.circle(leftFrame, (leftObjects[i][0], leftObjects[i][1]), 5, (0, 0, 255), -1)
        for i in range(len(rightObjects)):
            cv2.circle(rightFrame, (rightObjects[i][0], rightObjects[i][1]), 5, (0, 0, 255), -1)

        cv2.imshow('Image', largeFrame)
        cv2.imshow('Top Left', leftFrame)
        cv2.imshow('Bottom Right', rightFrame)

        stringToSend = ",".join([f"{x[0]},{x[1]}" for x in leftObjects])

        # Append a newline character to the string to indicate the end of the message
        stringToSend += '\n'

        # Send the string over serial
        ser.write(stringToSend.encode())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

vid.release()
cv2.destroyAllWindows()
