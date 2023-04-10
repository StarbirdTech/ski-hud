import cv2
import time
from pySerialTransfer import pySerialTransfer as txfer
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    link = None
    vid = None
    try:
        # link = txfer.SerialTransfer(lib.getSerialPort("Arduino"))

        # link.open()
        # time.sleep(5)  # allow some time for the Arduino to completely reset

        vid = cv2.VideoCapture(0)
        if not vid.isOpened():
            print("Cannot open camera")
            exit()
        
        plt.ion()

        # Create an empty plot with labels for the x and y axes
        fig, ax = plt.subplots()
        ax.set_xlabel('Time Segments')
        ax.set_ylabel('Time (Seconds)')

        # Create lists to store the time segments and the total time for each iteration
        segments = []
        total_times = []

        while (True):
            startTime = cv2.getTickCount()
            ret, frame = vid.read()
            if not ret:
                continue
            
            segment1 = startTime - cv2.getTickCount()

            # Convert the image to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Enhance the contrast and reduce the noise
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
            gray = cv2.medianBlur(gray, 5)
            # Apply Otsu's thresholding to segment the objects
            _, thresh = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            # Apply morphological opening to remove small objects
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            # Detect contours of the objects
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            getCntsTime = cv2.getTickCount()
            # print(contours)

            # contours.filter(lambda contour: 100 > cv2.contourArea(contour) > 5)

            segment2 = segment1 - cv2.getTickCount()

            objects = []
            # Loop through each contour
            for cnt in contours:
                # Compute the center position
                M = cv2.moments(cnt)
                objects.append(int(M['m10'] / M['m00']))
                objects.append(int(M['m01'] / M['m00']))

            segment3 = segment2 - cv2.getTickCount()
            
            total_time = segment1 + segment2 + segment3
    
            # Add the time segments and total time to the lists
            segments.append([segment1, segment2, segment3])
            total_times.append(total_time)

            # Update the plot with the new data
            ax.clear()
            ax.stackplot(range(len(total_times)), segments, labels=['Segment 1', 'Segment 2', 'Segment 3'])
            ax.set_title('Time Segments for While Loop')

            # Redraw the plot and pause briefly to allow time for the plot to be updated
            fig.canvas.draw()
            plt.pause(0.001)
            
            

    except KeyboardInterrupt:
        if link is not None:
            link.close()
        if vid is not None:
            vid.release()
        cv2.destroyAllWindows()

    except:
        import traceback
        traceback.print_exc()

        if link is not None:
            link.close()
        if vid is not None:
            vid.release()
        cv2.destroyAllWindows()
