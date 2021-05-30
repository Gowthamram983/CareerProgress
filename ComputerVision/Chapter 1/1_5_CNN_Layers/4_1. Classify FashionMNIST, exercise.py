# our basic libraries
import torch
import torchvision

# data loading and transforming
from torchvision.datasets import FashionMNIST
from torch.utils.data import DataLoader
from torchvision import transforms

# The output of torchvision datasets are PILImage images of range [0, 1].
# We transform them to Tensors for input into a CNN

## Define a transform to read the data in as a tensor
data_transform = transforms.ToTensor()

# choose the training and test datasets
train_data = FashionMNIST(root='./data', train=True,
                                   download=True, transform=data_transform)

test_data = FashionMNIST(root='./data', train=False,
                                  download=True, transform=data_transform)


# Print out some stats about the training and test data
print('Train data, number of images: ', len(train_data))
print('Test data, number of images: ', len(test_data))

# prepare data loaders, set the batch_size
## TODO: you can try changing the batch_size to be larger or smaller
## when you get to training your network, see how batch_size affects the loss
batch_size = 20

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

# specify the image classes
classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

import numpy as np
import matplotlib.pyplot as plt

# % matplotlib
# inline

# obtain one batch of training images
dataiter = iter(train_loader)
images, labels = dataiter.next()
images = images.numpy()

# plot the images in the batch, along with the corresponding labels
fig = plt.figure(figsize=(25, 4))
for idx in np.arange(batch_size):
 ax = fig.add_subplot(2, batch_size / 2, idx + 1, xticks=[], yticks=[])
 ax.imshow(np.squeeze(images[idx]), cmap='gray')
 ax.set_title(classes[labels[idx]])

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

 def __init__(self):
  super(Net, self).__init__()

  # 1 input image channel (grayscale), 10 output channels/feature maps
  # 3x3 square convolution kernel
  self.conv1 = nn.Conv2d(1, 10, 3)

  ## TODO: Define the rest of the layers:
  # include another conv layer, maxpooling layers, and linear layers
  # also consider adding a dropout layer to avoid overfitting

 ## TODO: define the feedforward behavior
 def forward(self, x):
  # one activated conv layer
  x = F.relu(self.conv1(x))

  # final output
  return x


# instantiate and print your Net
net = Net()
print(net)

import torch.optim as optim

## TODO: specify loss function (try categorical cross-entropy)
criterion = None

## TODO: specify optimizer
optimizer = None

from torch.autograd import Variable

# Calculate accuracy before training
correct = 0
total = 0

# Iterate through test dataset
for images, labels in test_loader:
 # warp input images in a Variable wrapper
 images = Variable(images)

 # forward pass to get outputs
 # the outputs are a series of class scores
 outputs = net(images)

 # get the predicted class from the maximum value in the output-list of class scores
 _, predicted = torch.max(outputs.data, 1)

 # count up total number of correct labels
 # for which the predicted and true labels are equal
 total += labels.size(0)
 correct += (predicted == labels).sum()

# calculate the accuracy
accuracy = 100 * correct / total

# print it out!
print('Accuracy before training: ', accuracy)

from torch.autograd import Variable


def train(n_epochs):
 for epoch in range(n_epochs):  # loop over the dataset multiple times

  running_loss = 0.0
  for batch_i, data in enumerate(train_loader):
   # get the input images and their corresponding labels
   inputs, labels = data

   # wrap them in a torch Variable
   inputs, labels = Variable(inputs), Variable(labels)

   # zero the parameter (weight) gradients
   optimizer.zero_grad()

   # forward pass to get outputs
   outputs = net(inputs)

   # calculate the loss
   loss = criterion(outputs, labels)

   # backward pass to calculate the parameter gradients
   loss.backward()

   # update the parameters
   optimizer.step()

   # print loss statistics
   running_loss += loss.data[0]
   if batch_i % 1000 == 999:  # print every 1000 mini-batches
    print('Epoch: {}, Batch: {}, Avg. Loss: {}'.format(epoch + 1, batch_i + 1, running_loss / 1000))
    running_loss = 0.0

 print('Finished Training')

# define the number of epochs to train for
n_epochs = 5 # start small to see if your model works, initially

# call train
train(n_epochs)

# initialize tensor and lists to monitor test loss and accuracy
test_loss = torch.zeros(1)
class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))

# set the module to evaluation mode
net.eval()

for batch_i, data in enumerate(test_loader):

 # get the input images and their corresponding labels
 inputs, labels = data

 # wrap them in a torch Variable
 # volatile means we do not have to track how the inputs change
 inputs, labels = Variable(inputs, volatile=True), Variable(labels, volatile=True)

 # forward pass to get outputs
 outputs = net(inputs)

 # calculate the loss
 loss = criterion(outputs, labels)

 # update average test loss
 test_loss = test_loss + ((torch.ones(1) / (batch_i + 1)) * (loss.data - test_loss))

 # get the predicted class from the maximum value in the output-list of class scores
 _, predicted = torch.max(outputs.data, 1)

 # compare predictions to true label
 correct = np.squeeze(predicted.eq(labels.data.view_as(predicted)))

 # calculate test accuracy for *each* object class
 # we get the scalar value of correct items for a class, by calling `correct[i].item()`
 for i in range(batch_size):
  label = labels.data[i]
  class_correct[label] += correct[i].item()
  class_total[label] += 1

 # calculate test accuracy for *each* object class
 for i in range(batch_size):
  label = labels.data[i]
  class_correct[label] += correct[i]
  class_total[label] += 1

print('Test Loss: {:.6f}\n'.format(test_loss.numpy()[0]))

for i in range(10):
 if class_total[i] > 0:
  print('Test Accuracy of %5s: %2d%% (%2d/%2d)' % (
   classes[i], 100 * class_correct[i] / class_total[i],
   np.sum(class_correct[i]), np.sum(class_total[i])))
 else:
  print('Test Accuracy of %5s: N/A (no training examples)' % (classes[i]))

print('\nTest Accuracy (Overall): %2d%% (%2d/%2d)' % (
 100. * np.sum(class_correct) / np.sum(class_total),
 np.sum(class_correct), np.sum(class_total)))

# obtain one batch of test images
dataiter = iter(test_loader)
images, labels = dataiter.next()
# get predictions
preds = np.squeeze(net(Variable(images, volatile=True)).data.max(1, keepdim=True)[1].numpy())
images = images.numpy()

# plot the images in the batch, along with predicted and true labels
fig = plt.figure(figsize=(25, 4))
for idx in np.arange(batch_size):
    ax = fig.add_subplot(2, batch_size/2, idx+1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(images[idx]), cmap='gray')
    ax.set_title("{} ({})".format(classes[preds[idx]], classes[labels[idx]]),
                 color=("green" if preds[idx]==labels[idx] else "red"))
# instantiate your Net
# this refers to your Net class defined above
net = Net()

# load the net parameters by name
# uncomment and write the name of a saved model
#net.load_state_dict(torch.load('saved_models/model_1.pt'))

print(net)

# Once you've loaded a specific model in, you can then
# us it or further analyze it!
# This will be especialy useful for feature visualization
