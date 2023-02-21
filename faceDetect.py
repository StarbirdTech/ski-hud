import cv2 as cv

faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while (True):
    ret, frame = cap.read()

    if ret == True:

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
          cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv.imshow('Frame', frame)

        # Press S on keyboard to stop the process
        if cv.waitKey(1) & 0xFF == ord('s'):
            break

    else:
        break

cap.release()
cv.destroyAllWindows()





