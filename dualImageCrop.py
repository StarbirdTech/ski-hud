import cv2

# Load the image
image = cv2.imread('test.jpg')

# Get the height and width of the image
height, width = image.shape[:2]

# Define the points from which the images will be cropped
top_left = (0, 0)  # (x, y)
bottom_right = (width, height)  # (x, y)

# Define the size of each cropped image
crop_top_left_size = (int(width/2), int(height/2))  # (width, height)
crop_bottom_right_size = (int(width/2), int(height/2))  # (width, height)

# Crop the image into two smaller images
crop_top_left = image[top_left[1]:top_left[1]+crop_top_left_size[1], top_left[0]:top_left[0]+crop_top_left_size[0]]
crop_bottom_right = image[bottom_right[1]-crop_bottom_right_size[1]:bottom_right[1], bottom_right[0]-crop_bottom_right_size[0]:bottom_right[0]]

# Display the cropped images
cv2.imshow('Top Left', crop_top_left)
cv2.imshow('Bottom Right', crop_bottom_right)
cv2.waitKey(0)
cv2.destroyAllWindows()
