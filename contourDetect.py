import cv2
import serial

ser = serial.Serial('COM4')
print(ser.name)

vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print("Cannot open camera")
    exit()

objects = []

while (True):
    ret, frame = vid.read()

    if ret == True:

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

            objects.append((center_x, center_y))
          
            # Draw the contour and center position on the image
            cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

        # Display the image
        cv2.imshow('Image', frame)

        #send object coordinates to arduino and clear objects list
        if len(objects) > 0:
            print(objects)
            ser.write(str(objects).encode())
            objects.clear()

        # Press S on keyboard to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    else:
        break

vid.release()
cv2.destroyAllWindows()
