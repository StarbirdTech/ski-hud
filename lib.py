from serial.tools import list_ports
import cv2


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


def getObjects(vid):
    frameW = int(vid.get(3))
    frameH = int(vid.get(4))
    frameRatio = frameW / frameH

    screenW = 128
    screenH = 64
    screenRatio = screenW / screenH
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

        objects = []
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

        # map the object positions to the screen
        screenObjects = []
        for obj in objects:
            screenObjects.append((int(obj[0] * screenRatio / frameRatio), int(obj[1] * screenRatio / frameRatio)))

        return screenObjects
    return None


if __name__ == "__main__":
    print(getSerialPort(input("Search String: ")))
