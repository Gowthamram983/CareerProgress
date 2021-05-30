import cv2 # computer vision library
import helpers

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Image data directories
image_dir_training = "day_night_images/training/"
image_dir_test = "day_night_images/test/"

# Using the load_dataset function in helpers.py
# Load training data
IMAGE_LIST = helpers.load_dataset(image_dir_training)

# Select an image and its label by list index
image_index = 120
selected_image = IMAGE_LIST[image_index][0]
selected_label = IMAGE_LIST[image_index][1]

# Display image and data about it
plt.imshow(selected_image)
plt.show()
print("Shape: "+str(selected_image.shape))
print("Label: " + str(selected_label))

# This function should take in an RGB image and return a new, standardized version
def standardize_input(image):
  ## TODO: Resize image so that all "standard" images are the same size 600x1100 (hxw)
  copy_image = np.copy(image)
  standard_im = copy_image[0:600,0:1100]

  return standard_im


# Examples:
# encode("day") should return: 1
# encode("night") should return: 0

def encode(label):
  numerical_val = 0
  ## TODO: complete the code to produce a numerical label
  if label == 'day':
   numerical_val = 1
  elif label == 'night':
   numerical_val = 0
  return numerical_val

def standardize(image_list):
   # Empty image data array
   standard_list = []

   # Iterate through all the image-label pairs
   for item in image_list:
    image = item[0]
    label = item[1]

    # Standardize the image
    standardized_im = standardize_input(image)

    # Create a numerical label
    binary_label = encode(label)

    # Append the image, and it's one hot encoded label to the full, processed list of image data
    standard_list.append((standardized_im, binary_label))

   return standard_list


# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)

# Display a standardized image and its label

# Select an image by index
image_num = 120
selected_image = STANDARDIZED_LIST[image_num][0]
selected_label = STANDARDIZED_LIST[image_num][1]

# Display image and data about it
## TODO: Make sure the images have numerical labels and are of the same size
plt.imshow(selected_image)
plt.show()
print("Shape: "+str(selected_image.shape))
print("Label [1 = day, 0 = night]: " + str(selected_label))
