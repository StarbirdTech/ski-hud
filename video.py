import cv2 as cv

cap = cv.VideoCapture('videoSource/lo6rBzkYw14.mp4')
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while (True):
    ret, frame = cap.read()

    if ret == True:

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        orb = cv.ORB_create(nfeatures=2000)
        kp, des = orb.detectAndCompute(gray, None)
        kp_image = cv.drawKeypoints(frame, kp, None, color=(0, 255, 0))

        #result.write(kp_image)
        cv.imshow('Frame', kp_image)

        # Press S on keyboard to stop the process
        if cv.waitKey(1) & 0xFF == ord('s'):
            break
        
    else:
        break

# When everything done, release
# the video capture and video
# write objects
cap.release()

# Closes all the frames
cv.destroyAllWindows()

print("The video was successfully saved")

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # Our operations on the frame come here
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     orb = cv.ORB_create(nfeatures=2000)
#     kp, des = orb.detectAndCompute(gray, None)

# # Drawing the keypoints
#     kp_image = cv.drawKeypoints(frame, kp, None, color=(0, 255, 0), flags=0)
#     # Display the resulting frame
#     cv.imshow('frame', kp_image)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()