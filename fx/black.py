import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the image
image = mpimg.imread('img/1.png')

# Convert to grayscale using luminance formula (standard for color to grayscale)
# 0.299 * R + 0.587 * G + 0.114 * B
gray_image = np.dot(image[...,:3], [0.299, 0.587, 0.114])

# Save the result
plt.imsave('img/2.jpg', gray_image, cmap='gray')