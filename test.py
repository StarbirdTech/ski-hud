import cv2
 
# Read the original image
img = cv2.imread('test1.jpg') 
# Display original image
cv2.imshow('Original', img)
cv2.waitKey(0)
 
# convert the image to grayscale format
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply binary thresholding
ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
# visualize the binary image
cv2.imshow('Binary image', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
