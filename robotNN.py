import robot
import numpy as np

class RobotNN():
    def _init_(self, layers, n_nodes, activation_function):
        self.layers = layers
        self.inputLayer = []
        self.hiddenLayer = []
        self.outputLayer = []
        self.n_nodes = n_nodes
        self.activation_function = activation_function
    
    def layers(self):
        pass

    
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output
 

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
