import cv2
from pySerialTransfer import pySerialTransfer as txfer
from lib import getSerialPort

#cap = cv2.VideoCapture('./lowResSample.mp4')
cap = cv2.VideoCapture(0)

#link = txfer.SerialTransfer(getSerialPort("Arduino"))

ret, frame1 = cap.read()
frame1 = cv2.resize(frame1, (128, 64))

while True:
    ret, frame2 = cap.read()

    if not ret:
        break
    frame2 = cv2.resize(frame2, (128, 64))
    output = cv2.cvtColor(cv2.absdiff(frame1, frame2), cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('OpenCV - Highlight', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame1 = frame2

    print(output)

cap.release()
cv2.destroyAllWindows()
