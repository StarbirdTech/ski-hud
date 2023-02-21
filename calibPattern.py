import numpy as np
import cv2

# Define the size of the chessboard pattern
pattern_size = (7, 6)

# Generate the object points for the chessboard corners
object_points = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
object_points[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

# Generate a chessboard pattern image
pattern_image = np.zeros((500, 500), dtype=np.uint8)
cv2.drawChessboardCorners(pattern_image, pattern_size, object_points, True)

# Save the pattern image
cv2.imwrite('calibration_pattern.jpg', pattern_image)
