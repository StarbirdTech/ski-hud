import cv2
import numpy as np

# Load image
img = cv2.imread('./test1.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Compute gradient
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
grad = np.sqrt(sobelx**2 + sobely**2)

# Compute angle
theta = np.arctan2(sobely, sobelx)
theta = np.degrees(theta) % 180

# Define refractive index
refractive_index = 1.5

# Compute reflection coefficient
cos_theta = np.cos(np.radians(theta))
sin_theta = np.sin(np.radians(theta))
sin_theta_t = sin_theta / refractive_index
cos_theta_t = np.sqrt(1 - sin_theta_t**2)

# Handle divide by zero
zero_mask = grad == 0
sin_theta_t[zero_mask] = 0
cos_theta_t[zero_mask] = 1

reflection_coefficient = 0.5 * ((sin_theta - refractive_index * sin_theta_t)**2 / (cos_theta + refractive_index * cos_theta_t)**2 + (cos_theta - refractive_index * cos_theta_t)**2 / (sin_theta + refractive_index * sin_theta_t)**2)

# Apply Fresnel effect
fresnel = reflection_coefficient[:, :, np.newaxis]
result = img * fresnel + (1 - fresnel) * gray[:, :, np.newaxis]

# Show result
cv2.imshow('Fresnel effect', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
