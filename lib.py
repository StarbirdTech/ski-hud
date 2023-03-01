from serial.tools import list_ports
import cv2
import numpy as np


def getSerialPort(searchString):
    # check if there is a serial port with the given search string
    # if there are multiple matches, ask the user to select one
    # return the selected port
    # if no port found, print error and exit

    serialPorts = list(list_ports.comports())
    ports = []
    for port in serialPorts:
        if searchString in port[1]:
            ports.append(port[0])
    if len(ports) == 0:
        print("No serial port found with search string: " + searchString)
        print("Exiting...")
        exit()
    elif len(ports) == 1:
        return ports[0]
    else:
        print("Multiple serial ports found:")
        for i in range(len(ports)):
            print(str(i) + ": " + ports[i])
        return ports[int(input())]


def getObjects(vid, debug=False):
    frameW = int(vid.get(3))
    frameH = int(vid.get(4))
    frameRatio = frameW / frameH

    screenMargin = 32
    screenW = 128
    screenH = 64
    dualScreenW = screenW*2 + screenMargin
    dualScreenH = screenH

    ret, frame = vid.read()

    if ret == True:
        # scale down the frame to a width of dualScreenW
        frame = cv2.resize(frame, (dualScreenW, int(dualScreenW/frameRatio)))

        # get the new frame dimensions
        frameW = frame.shape[1]
        frameH = frame.shape[0]

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

        # draw contours
        if debug:
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        objects = []
        # Loop through each contour
        for cnt in contours:
            # Filter out small or spurious contours
            if cv2.contourArea(cnt) < 5:
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

        leftScreenBounds = [[0, screenW], [frameH/2 - screenH/2, frameH/2 + screenH/2]]
        rightScreenBounds = [[frameW-screenW, frameW], [frameH/2 - screenH/2, frameH/2 + screenH/2]]

        # left objects is all objects that are within left screen bounds
        leftObjects = [obj for obj in objects if obj[0] >= leftScreenBounds[0][0] and obj[0] <= leftScreenBounds[0][1] and obj[1] >= leftScreenBounds[1][0] and obj[1] <= leftScreenBounds[1][1]]
        # right objects is all objects that are within right screen bounds
        rightObjects = [obj for obj in objects if obj[0] >= rightScreenBounds[0][0] and obj[0] <= rightScreenBounds[0][1] and obj[1] >= rightScreenBounds[1][0] and obj[1] <= rightScreenBounds[1][1]]

        if debug:
            # left screen objects
            for i in range(0, len(leftObjects)):
                cv2.circle(frame, leftObjects[i], 5, (0, 255, 0), -1)
                cv2.putText(frame, str(i), leftObjects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            # right screen objects
            for i in range(0, len(rightObjects)):
                cv2.circle(frame, rightObjects[i], 5, (255, 0, 0), -1)
                cv2.putText(frame, str(i), rightObjects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            # draw objects not in left or right screen and label with index
            for i in range(0, len(objects)):
                if objects[i] not in leftObjects and objects[i] not in rightObjects:
                    cv2.circle(frame, objects[i], 5, (0, 0, 255), -1)
                    cv2.putText(frame, str(i), objects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        # return the left and right objects like this [[left objects], [right objects]]
        # remove the tuples
        return [list(map(list, leftObjects)), list(map(list, rightObjects))]
    return None


def getObjectsNew(vid, debug=False):
    frameW = int(vid.get(3))
    frameH = int(vid.get(4))
    frameRatio = frameW / frameH

    screenMargin = 32
    screenW = 128
    screenH = 64
    dualScreenW = screenW*2 + screenMargin
    dualScreenH = screenH

    ret, frame = vid.read()

    if ret == True:
        # scale down the frame to a width of dualScreenW
        frame = cv2.resize(frame, (dualScreenW, int(dualScreenW/frameRatio)))

        # get the new frame dimensions
        frameW = frame.shape[1]
        frameH = frame.shape[0]

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

        objects = []
        # Loop through each contour
        for cnt in contours:
            # Filter out small or spurious contours
            if cv2.contourArea(cnt) < 5:
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

        leftScreenBounds = [[0, screenW], [frameH/2 - screenH/2, frameH/2 + screenH/2]]
        rightScreenBounds = [[frameW-screenW, frameW], [frameH/2 - screenH/2, frameH/2 + screenH/2]]

        leftObjects = []
        rightObjects = []

        for obj in objects:
            if obj[0] > leftScreenBounds[0][0] and obj[0] < leftScreenBounds[0][1] and obj[1] > leftScreenBounds[1][0] and obj[1] < leftScreenBounds[1][1]:
                leftObjects.append(obj)
            elif obj[0] > rightScreenBounds[0][0] and obj[0] < rightScreenBounds[0][1] and obj[1] > rightScreenBounds[1][0] and obj[1] < rightScreenBounds[1][1]:
                rightObjects.append(obj)

        if debug:
            # left screen objects
            for i in range(0, len(leftObjects)):
                cv2.circle(frame, leftObjects[i], 5, (0, 255, 0), -1)
                cv2.putText(frame, str(i), leftObjects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            # right screen objects
            for i in range(0, len(rightObjects)):
                cv2.circle(frame, rightObjects[i], 5, (255, 0, 0), -1)
                cv2.putText(frame, str(i), rightObjects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            # draw objects not in left or right screen and label with index
            for i in range(0, len(objects)):
                if objects[i] not in leftObjects and objects[i] not in rightObjects:
                    cv2.circle(frame, objects[i], 5, (0, 0, 255), -1)
                    cv2.putText(frame, str(i), objects[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        return [leftObjects, rightObjects]
    return None



if __name__ == "__main__":
    print(getSerialPort(input("Search String: ")))
