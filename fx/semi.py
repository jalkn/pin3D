import cv2

# Load the image
image = cv2.imread('img/1.png')

# Convert to grayscale (semitone)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save the result
cv2.imwrite('fx/1.jpg', gray_image)