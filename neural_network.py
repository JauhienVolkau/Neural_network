# -*- coding: utf-8 -*-

import numpy as np
import random
from keras.datasets import mnist
from matplotlib import pyplot
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import cv2 
from google.colab.patches import cv2_imshow

def ReLU(vector):
  return vector*(vector>0)

def softmax(vector):
  e_i = np.exp(vector)
  return e_i/e_i.sum()

class OurNeuralNetwork:
  '''
  The structure of NN:
    - input layer with 784 neurons (x1, ... , x784)
    - activation function: ReLU
    - hidden layer with 128 neurons (h1, ... , h128)
    - activation function:: softmax
    - output layer with 11 neurons (o1, ... , o11)

    - loss function: Cross Entropy Loss
    - updating weights and biases: Nesterov Accelerated Gradient Descent Method
  '''
  def __init__(self):

    # initializing weights and biases
    self.W1 = np.array([[random.uniform(-0.0001, 0.0001) for i in range(784)] for j in range(128)])
    self.b1 = np.zeros(128) #np.array([random.uniform(-0.001, 0.001) for j in range(128)])
    self.W2 = np.array([[random.uniform(-0.0001, 0.0001) for i in range(128)] for j in range(11)])
    self.b2 = np.zeros(11) #np.array([random.uniform(-0.001, 0.001) for j in range(11)])

    self.learning_rate = 0.0001  # learning rate
    self.momentum = 0.9  # gamma constant for NAG
    self.epochs = 100  # number of epochs
    self.batch_size = 40

  def training(self, X, Y, X_val, Y_val):
   
    # possible modes: training/validation

    # Identity matrix
    E = np.eye(11)

    CE = {'training': [], 'validation': []}  # cross entropy loss by epochs

    for epoch in tqdm(range(self.epochs)):

      for mode in ['training', 'validation']:

        CE_total = 0  # cross entropy loss for 1 epoch
      
        if mode=='training':
          # v_t-1 - velocity on the previous step 
          prev_v_b1 = np.zeros(128) 
          prev_v_W1 = np.zeros((128,784))
          prev_v_b2 = np.zeros(11)
          prev_v_W2 = np.zeros((11,128))
          n = len(X)
        else:
          n = len(X_val)

        for i in range((n - 1) // self.batch_size + 1):
          if mode=='training':
            # creating a batch of data in training mode
            start_i = i * self.batch_size
            end_i = start_i + self.batch_size
            Xb = X[start_i:end_i]
            Yb = Y[start_i:end_i]

            # v_t - velocity on the next step 
            v_b1 = self.momentum*prev_v_b1
            v_W1 = self.momentum*prev_v_W1
            v_b2 = self.momentum*prev_v_b2
            v_W2 = self.momentum*prev_v_W2

            # saving current parameters of our NN
            prev_W1 = self.W1
            prev_b1 = self.b1
            prev_W2 = self.W2
            prev_b2 = self.b2

            # counting new parameters of NN
            self.W1 -= v_W1
            self.b1 -= v_b1
            self.W2 -= v_W2
            self.b2 -= v_b2

            # initializing gradients
            dCE_db1 = np.zeros(128) 
            dCE_db2 = np.zeros(11)
            dCE_dW1 = np.zeros((128,784))
            dCE_dW2 = np.zeros((11,128))
          else:
            # creating a batch of data in validation mode
            start_i = i * self.batch_size
            end_i = start_i + self.batch_size
            Xb = X_val[start_i:end_i]
            Yb = Y_val[start_i:end_i]

          for x,y in zip(Xb,Yb):
            # feed_forward
            h_ = self.W1.dot(x)+self.b1
            h = ReLU(h_)
            z = self.W2.dot(h)+self.b2
            output = softmax(z)

            CE_total += np.log(output[y])

            if mode=='training':
              # counting gradients
              dCE_db2 += output-E[y]
              dCE_dW2 += ((output-E[y]).reshape((11,1))).dot(h.reshape((128,1)).T)
              dCE_db1 += (self.W2-self.W2[y]).T.dot(output)*(h>0) #.reshape((11,1))
              dCE_dW1 += (((self.W2-self.W2[y]).T.dot(output)*(h>0)).reshape((128,1))).dot(x.reshape((784,1)).T)

          if mode=='training':
            self.W1 = prev_W1
            self.W2 = prev_W2
            self.b1 = prev_b1
            self.b2 = prev_b2

            v_W1 += self.learning_rate*dCE_dW1
            v_W2 += self.learning_rate*dCE_dW2
            v_b1 += self.learning_rate*dCE_db1
            v_b2 += self.learning_rate*dCE_db2

            # updating gradients
            self.W1 -= v_W1
            self.W2 -= v_W2
            self.b1 -= v_b1
            self.b2 -= v_b2

            prev_v_b1 = v_b1
            prev_v_b2 = v_b2
            prev_v_W1 = v_W1
            prev_v_W2 = v_W2

        CE_total *=(-1.)
        CE[mode].append(CE_total)

        if mode=='training':
          print(f'epoch № {epoch}, CE_loss = {CE_total}')
          print(f"output = {output}")
        
        if mode=='training' and epoch%10==0:
          print(f"W1 = {self.W1}")
          print(f"b1 = {self.b1}")
          print(f"W2 = {self.W2}")
          print(f"b2 = {self.b2}")

    return CE

  def predict(self,x,y):
    output = softmax(self.W2.dot(ReLU(self.W1.dot(x)+self.b1))+self.b2)
    answ = np.argmax(output)
    return 'None' if answ==10 else answ

# loading training and validation datasets
(train_X, train_y), (test_X, test_y) = mnist.load_data()

# visualization of 3 first images
for i in range(3):  
  pyplot.subplot(330 + 1 + i)
  pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))
  pyplot.show()

# data scaling and converting to another shape
train_X_scal_resh = train_X.reshape((train_X.shape[0], 784))
train_X_scal_resh = (train_X_scal_resh-128.)/256.
test_X_scal_resh = test_X.reshape((test_X.shape[0], 784))
test_X_scal_resh = (test_X_scal_resh-128.)/256.

network = OurNeuralNetwork()

# network.learning_rate = 0.0001
# network.momentum = 0.85
# network.batch_size = 50
# network.epochs = 100

# training
%%time
CE_loss = network.training(train_X_scal_resh, train_y, test_X_scal_resh, test_y)

# CE_loss

plt.figure(figsize=(10, 8))
plt.plot(CE_loss['training'], label="Train", color="blue")
plt.plot(CE_loss['validation'], label="Validation", color="orange")
plt.legend(frameon=True)
plt.ylabel("Cross Entropy Loss")
plt.xlabel("Epoch");

# some predictions

for i in range(3):
  ind = random.randint(0, train_X.shape[0])
  pyplot.subplot(330 + 1+i)
  pyplot.imshow(train_X[ind], cmap=pyplot.get_cmap('gray'))
  pyplot.show()

  train_X_pred = train_X[ind].reshape(784)
  train_X_pred = (train_X_pred-128.)/256.
  prediction = network.predict(train_X_pred, train_y[ind])
  print(f"true digit: {train_y[ind]}")
  print(f"predicted digit: {prediction}")
  print()
