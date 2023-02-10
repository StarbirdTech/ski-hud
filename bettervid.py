import cv2

vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print("Cannot open camera")
    exit()

while (True):
    ret, frame = vid.read()

    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create SIFT object
        sift = cv2.SIFT_create()

        # Detect keypoints
        keypoints = sift.detect(gray, None)

        # Draw keypoints
        img_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Iterate through keypoints and draw the center as a single point
        for keypoint in keypoints:
            x, y = keypoint.pt
            center = (int(x), int(y))
            cv2.circle(img_with_keypoints, center, 1, (0, 0, 255), 2)

        # Display the image
        cv2.imshow("Features", img_with_keypoints)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    else:
        break

vid.release()

cv2.destroyAllWindows()
