import cv2
import lib
import time
from pySerialTransfer import pySerialTransfer as txfer

run = True
debug = True

sourceLocation = 0
mediaSource = cv2.VideoCapture(0)

if mediaSource.isOpened():
    if serialPort := lib.getSerialPort("Arduino"):
        serialLink = txfer.SerialTransfer(serialPort)
        serialLink.open()
        time.sleep(5)
    else:
        if not debug:
            run = False
else:
    run = False
    if type(sourceLocation) is int:
        print(f"Cannot open camera {sourceLocation}")
    elif type(sourceLocation) is str:
        print(f"Cannot open video {sourceLocation}")
    else:
        print("mediaSource is incorrect type")

while run:
    if objects := lib.getObjects(mediaSource, debug=True):
        print("left: {}".format(objects[0]))
        print("right: {}".format(objects[1]))
        payload = serialLink.tx_obj([y for x in objects[0] for y in x])
        serialLink.send(payload)
        time.sleep(0.01)
    else:
        print("none")

print("Exiting...")
if mediaSource:
    mediaSource.release()
    print("✅  mediaSource closed")
else:
    print("🟨  no mediaSource found")
if serialLink:
    serialLink.close()
    print("✅  serialLink closed")
else:
    print("🟨  no serialLink found")
cv2.destroyAllWindows()
