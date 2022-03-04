import robot
import numpy as np
import random

class RobotNN():
    def _init_(self):
        self.num_inputs = 10
        self.num_hidden = 4
        self.num_outputs = 2
        #setting our layers
        layers = [self.num_inputs] + [self.num_hidden] + [self.num_outputs]

        #random weights and biases
        weights = []
        biases = []
        for i in range(len(layers)-1):
            w = np.random.rand(layers[i], layers[i+1])
            weights.append(w)
            b = np.zeros(layers[i])
            biases.append(b)
        self.weights = weights
        self.biases = biases
    
        #create activations 
        activations =[]
        for i in range(len(layers)):
            a = np.zeros(layers[i])
            activations.append(a)
        self.activations = activations    
    
    #implement forwardpropagation
    def forward_propagate(self,inputs):      
        # the input layer activation is just the input itself
        activations = inputs
        for i, w in enumerate(self.weights):
            #calculate the net inputs
            net_inputs = np.dot(activations, w)
            #calculate the activations
            #activation of the sigmoid function ==> f(x) = 1/(1+e^(-x)) 
            activations = 1.0/(1+np.exp(-net_inputs))
            # save the activations for backpropogation
            self.activations[i + 1] = activations
            print(activations)
        return activations
        


 

class RobotEA():
    def __init__(self):
        pass

    def evaluate(self):
        pass

    def selection(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass


#if _name_ == '_main_':
 #   Network(Layer(10, 'relu'), Layer(4, 'relu'), Layer(2, 'linear'))
