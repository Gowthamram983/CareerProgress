import matplotlib.pyplot as plt
import numpy as np
import cv2

#Read image using opencv imread
image = cv2.imread(r"C:\Users\Gowtham\Documents\Udacity\1_1_Image_Representation\images\pizza_bluescreen.jpg")

#print dimension
print("Type of data",type(image),
      "Dimensions",image.shape)

#copy image
image_copy = np.copy(image)

#change color
image_copy = cv2.cvtColor(image_copy,cv2.COLOR_BGR2RGB)

#disply image
plt.imshow(image_copy)
plt.show()

#define color selection boundaries in RGB Values
lower_blue = np.array([0,0,230])
upper_blue = np.array([50,50,255])

#masking
mask = cv2.inRange(image_copy,lower_blue,upper_blue)

#virtualize mask
plt.imshow(mask,cmap= 'gray')
plt.show()

#masked image
masked_image = np.copy(image_copy)
masked_image[mask!=0] = [0,0,0]

plt.imshow(masked_image)
plt.show()

# Load in a background image, and convert it to RGB
background_image = cv2.imread('images/space_background.jpg')
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)

# Crop it to the right size (514x816)
crop_background = background_image[0:514, 0:816]

# Mask the cropped background so that the pizza area is blocked
crop_background[mask == 0] = [0, 0, 0]

# Display the background
plt.imshow(crop_background)
plt.show()

# Add the two images together to create a complete image!
complete_image = masked_image + crop_background

# Display the result
plt.imshow(complete_image)
plt.show()
