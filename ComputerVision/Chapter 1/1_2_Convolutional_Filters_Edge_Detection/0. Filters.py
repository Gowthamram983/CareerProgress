import numpy as np
import matplotlib.pyplot as plt
import cv2

image = cv2.imread('images/city_hall.jpg')

image_copy = np.copy(image)

image_copy = cv2.cvtColor(image_copy,cv2.COLOR_BGR2RGB)

plt.imshow(image_copy)
plt.show()

gray = cv2.cvtColor(image_copy,cv2.COLOR_RGB2GRAY)

plt.imshow(gray,cmap = 'gray')
plt.show()

#custom edge detection filter to detect vertical edges
#sobel filter finds the abrupt changes in x,y directions seperately
sobel_x = np.array([ [-1 ,0,1],
                    [-2 ,0,2],
                    [ -1,0,1]])

# -1 refers to provide same type as input image.
#three arguments are grayscale image, bit-depth, kernel/filter convolution
filtered_image = cv2.filter2D(gray,-1,sobel_x)

plt.imshow(filtered_image,cmap = 'gray')
plt.show()

#Change the threshold values from 100 to any data to see sharper edges in results.
retval, binary_image = cv2.threshold(filtered_image,100,255,cv2.THRESH_BINARY)

plt.imshow(binary_image,cmap = 'gray')
plt.show()

#note: low pass filters are used before high pass filters to reduce noise.
