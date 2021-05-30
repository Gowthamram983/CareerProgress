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
image_index = 0
selected_image = IMAGE_LIST[image_index][0]
selected_label = IMAGE_LIST[image_index][1]

## TODO: Print out 1. The shape of the image and 2. The image's label `selected_label`
print("Shape: "+str(selected_image.shape))
print("Label: " + str(selected_label))

## TODO: Display a night image

# image_index = 121
# selected_image = IMAGE_LIST[image_index][0]
# selected_label = IMAGE_LIST[image_index][1]

# print("Shape: "+str(selected_image.shape))
# print("Label: " + str(selected_label))
print(IMAGE_LIST[image_index][0])
print(len(IMAGE_LIST))




