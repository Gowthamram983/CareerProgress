import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np
import cv2

# Read in the image
image = mpimg.imread('images/car_green_screen.jpg')

# Print out the image dimensions (height, width, and depth (color))
print('Image dimensions:', image.shape)

# Display the image
# plt.imshow(image)
# plt.show()

## TODO: Define our color selection boundaries in RGB values
lower_green = np.array([0,230,0])
upper_green = np.array([200,255,200])

# Define the masked area
mask = cv2.inRange(image, lower_green, upper_green)

# Vizualize the mask
# plt.imshow(mask, cmap='gray')
# plt.show()

# Mask the image to let the car show through
masked_image = np.copy(image)

masked_image[mask != 0] = [0, 0, 0]

# Display it!
plt.imshow(masked_image)
plt.show()

# Load in a background image, and convert it to RGB
background_image = mpimg.imread('images/sky.jpg')

## TODO: Crop it or resize the background to be the right size (450x660)
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
crop_background = background_image[0:450, 0:660]

## TODO: Mask the cropped background so that the pizza area is blocked
# Hint mask the opposite area of the previous image
crop_background[mask == 0] = [255, 255, 255]
## TODO: Display the background and make sure

# Add the two images together to create a complete image!
complete_image = masked_image + crop_background

# Display the result
plt.imshow(complete_image)
plt.show()