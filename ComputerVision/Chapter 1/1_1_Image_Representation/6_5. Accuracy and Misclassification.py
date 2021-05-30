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

# Standardize all training images
STANDARDIZED_LIST = helpers.standardize(IMAGE_LIST)

# Display a standardized image and its label

# Select an image by index
image_num = 0
selected_image = STANDARDIZED_LIST[image_num][0]
selected_label = STANDARDIZED_LIST[image_num][1]

# Display image and data about it
plt.imshow(selected_image)
print("Shape: "+str(selected_image.shape))
print("Label [1 = day, 0 = night]: " + str(selected_label))


# Find the average Value or brightness of an image
def avg_brightness(rgb_image):
  # Convert image to HSV
  hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

  # Add up all the pixel values in the V channel
  sum_brightness = np.sum(hsv[:, :, 2])
  area = 600 * 1100.0  # pixels

  # find the avg
  avg = sum_brightness / area

  return avg


# This function should take in RGB image input
def estimate_label(rgb_image):
  # TO-DO: Extract average brightness feature from an RGB image
  avg = avg_brightness(rgb_image)

  # Use the avg brightness feature to predict a label (0, 1)
  predicted_label = 0
  # TO-DO: Try out different threshold values to see what works best!
  threshold = 97
  if (avg > threshold):
   # if the average brightness is above the threshold value, we classify it as "day"
   predicted_label = 1
  # else, the predicted_label can stay 0 (it is predicted to be "night")

  return predicted_label

import random

# Using the load_dataset function in helpers.py
# Load test data
TEST_IMAGE_LIST = helpers.load_dataset(image_dir_test)

# Standardize the test data
STANDARDIZED_TEST_LIST = helpers.standardize(TEST_IMAGE_LIST)

# Shuffle the standardized test data
random.shuffle(STANDARDIZED_TEST_LIST)

# Constructs a list of misclassified images given a list of test images and their labels
def get_misclassified_images(test_images):
  # Track misclassified images by placing them into a list
  misclassified_images_labels = []

  # Iterate through all the test images
  # Classify each image and compare to the true label
  for image in test_images:

   # Get true data
   im = image[0]
   true_label = image[1]

   # Get predicted label from your classifier
   predicted_label = estimate_label(im)

   # Compare true and predicted labels
   if (predicted_label != true_label):
    # If these labels are not equal, the image has been misclassified
    misclassified_images_labels.append((im, predicted_label, true_label))

  # Return the list of misclassified [image, predicted_label, true_label] values
  return misclassified_images_labels

# Find all misclassified images in a given test set
MISCLASSIFIED = get_misclassified_images(STANDARDIZED_TEST_LIST)

# Accuracy calculations
total = len(STANDARDIZED_TEST_LIST)
num_correct = total - len(MISCLASSIFIED)
accuracy = num_correct/total

print('Accuracy: ' + str(accuracy))
print("Number of misclassified images = " + str(len(MISCLASSIFIED)) +' out of '+ str(total))

# Visualize misclassified example(s)
num = 0

for num in range(0,13):
  test_mis_im = MISCLASSIFIED[num][0]
  test_mis_im_label = MISCLASSIFIED[num][1]

  ## TODO: Display an image in the `MISCLASSIFIED` list
  plt.imshow(test_mis_im)
  plt.show()
  ## TODO: Print out its predicted label
  print("Shape: "+str(test_mis_im.shape))
  print("Label [1 = day, 0 = night]: " + str(test_mis_im_label))

  ## to see what the image *was* incorrectly classified as