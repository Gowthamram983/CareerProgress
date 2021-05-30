import numpy as np
import matplotlib.image as mpimg  # for reading in images

import matplotlib.pyplot as plt
import cv2  # computer vision library

# Read in the image
image = plt.imread(r'C:\Users\Gowtham\Documents\Udacity\1_1_Image_Representation\images\waymo_car.jpg') #edited by G_RAM

# Print out the image dimensions
print('Image dimensions:', image.shape)

# Change from color to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# plt.imshow(gray_image, cmap='gray')
c = plt.imshow(gray_image,cmap='gray')
# plt.colorbar(c)
# plt.title('matplotlib.pyplot.imshow() function Example',
#                                      fontweight ="bold")
plt.show()

# Print specific grayscale pixel values
# What is the pixel value at x = 400 and y = 300 (on the body of the car)?

x = 400
y = 300

print(gray_image[y,x])

#Find the maximum and minimum grayscale values in this image

max_val = np.amax(gray_image)
min_val = np.amin(gray_image)

print('Max: ', max_val)
print('Min: ', min_val)

tiny_image = np.array([[0, 20, 30, 150, 120],
                      [200, 200, 250, 70, 3],
                      [50, 180, 85, 40, 90],
                      [240, 100, 50, 255, 10],
                      [30, 0, 75, 190, 220]])

# To show the pixel grid, use matshow
plt.matshow(tiny_image, cmap='gray')
plt.show()

## TODO: See if you can draw a tiny smiley face or something else!
tiny_image1 = np.array([[0, 0, 0, 0, 0,0],
                      [0, 255, 0, 0, 255,0],
                      [0, 0, 0, 0, 0,0],
                      [0, 0, 255, 255, 0,0],
                      [0,0,0,0,0,0],
                      [0,255,0,0,255,0],
                      [0,0,255,255,0,0],
                      [0,0,0,0,0,0]])

plt.matshow(tiny_image1, cmap='gray')
plt.show()