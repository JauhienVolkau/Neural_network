# Neural network for handwritten digits recognition
____
## TASK
RECOGNITION OF HANDWRITTEN DIGITS
- To write a class for a model with the following architecture:
    - 1 input layer with 28x28 neurons (activation function is ReLU)
    - 1 hidden layer with 128 neurons (activation function is softmax)
    - 1 output layer with 11 neurons (the 11th neuron is needed to make it possible in future to detect a case when the model can't recognize a symbol as a digit)
- The output is a digit 0-9 or none
- Loss function is CrossEntropy (CE)
- Updating weights: Nesterov Accelerated Gradient method (NAG)
- Stack: only basic libraries are allowed (such as pandas, numpy and others); pytorch, tensorflow and similar libraries can not be used
- Plot loss function by epochs for train and validation modes
____
## INSTALLATION
Make sure that all libraries from *requirements.txt* are installed on your machine.  
There are 3 ways to run this project:  
**I**. Download ***neural_network.py*** and create a project in any IDE for Python (for example PyCharm or IDLE)  
**II**. Download ***neural_network.ipynb*** and open it in Google Colab (online)  
**III**. If you use Docker, you can download and run the project by doing these commands:
- ***docker pull jauhienvolkau/nn:mytag***
- ***docker run jauhienvolkau/nn:mytag***  
**IV**. You can use saved weights if you don't want to train a model. You need to download all files from the corresponding folder and save them to the same folder as file with the source code. Then in your project comment lines 188-198 from  ***neural_network.py*** and paste
```python
    network.W1 = np.load('W1.npz')
    network.b1 = np.load('b1.npz')
    network.W2 = np.load('W2.npz')
    network.b2 = np.load('b2.npz')
```
____
