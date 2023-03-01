import serial
import lib
import time
import cv2

#port = lib.getSerialPort("Arduino")
#ser = serial.Serial(port, 9600)


leftSerial = serial.Serial(lib.getSerialPort("Arduino"), 9600)
rightSerial = serial.Serial(lib.getSerialPort("Arduino"), 9600)
time.sleep(5)

vid = cv2.VideoCapture("lowResSample.mp4")
if not vid.isOpened():
    print("Cannot open camera")
    exit()

try:
    while (True):
        if data := lib.getObjects(vid, debug=True):
            leftData = data[0]
            # flatten the list
            leftData = [item for sublist in leftData for item in sublist]
            # divide all numbers in data by 2
            leftData = [int(x/2) for x in leftData]
            # reverse the order of 0, 2, 4, 6, 8, 10 and 1, 3, 5, 7, 9, 11
            # remove values or add zeros to make data 12 elements long
            if len(leftData) > 12:
                leftData = leftData[:12]
            elif len(leftData) < 12:
                leftData += [0 for _ in range(12 - len(leftData))]
            # change 0,1,2,3... to 1,0,3,2...
            for i in range(0, len(leftData), 2):
                leftData[i], leftData[i+1] = leftData[i+1], leftData[i]

            rightData = data[1]
            # flatten the list
            rightData = [item for sublist in rightData for item in sublist]
            # divide all numbers in data by 2
            rightData = [int(x/2) for x in rightData]
            # reverse the order of 0, 2, 4, 6, 8, 10 and 1, 3, 5, 7, 9, 11
            # remove values or add zeros to make data 12 elements long
            if len(rightData) > 12:
                rightData = rightData[:12]
            elif len(rightData) < 12:
                rightData += [0 for _ in range(12 - len(rightData))]
            # change 0,1,2,3... to 1,0,3,2...
            for i in range(0, len(rightData), 2):
                rightData[i], rightData[i+1] = rightData[i+1], rightData[i]
        else:
            leftData = [0 for _ in range(12)]
            rightData = [0 for _ in range(12)]

        print(str(leftData))
        leftSerial.write(str(leftData).encode())
        print(str(rightData))
        rightSerial.write(str(rightData).encode())
except KeyboardInterrupt:
    print("Exiting...")
except:
    import traceback
    traceback.print_exc()
finally:
    leftSerial.close()
    rightSerial.close()
    vid.release()
    cv2.destroyAllWindows()
