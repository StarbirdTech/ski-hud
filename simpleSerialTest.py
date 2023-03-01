import serial
import lib
import time
import cv2

port = lib.getSerialPort("Arduino")
ser = serial.Serial(port, 9600)
time.sleep(5)
print("Connected to " + port)

vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print("Cannot open camera")
    exit()

try:
    while (True):
        if data := lib.getObjects(vid, debug=True):
            data = data[0]
            # flatten data
            data = [y for x in data for y in x]
            # remove values or add zeros to make data 12 elements long
            if len(data) > 12:
                data = data[:12]
            elif len(data) < 12:
                data += [0 for _ in range(12 - len(data))]
        else:
            data = [0 for _ in range(12)]

        print(str(data))
        ser.write(str(data).encode())
except KeyboardInterrupt:
    print("Exiting...")
except:
    import traceback
    traceback.print_exc()
finally:
    ser.close()
    vid.release()
    cv2.destroyAllWindows()
