import numpy as np


class network():
    def __init__(self, weights=None):
        self.num_inputs = 16
        self.num_hidden = 4
        self.num_outputs = 2
        self.feedback = [0, 0, 0, 0]
        self.weights = weights

        if weights is None:
            self.hidden_layer1 = network.layer(16, 4)
            self.act_sigmoid1 = network.Activation_Sigmoid()
            self.output_layer2 = network.layer(4, 2)
            self.act_tanh = network.Activation_Tanh()
            self.weights = [self.hidden_layer1.weights, self.output_layer2.weights]
        else:
            self.hidden_layer1 = network.layer(16, 4, self.weights[0])
            self.act_sigmoid1 = network.Activation_Sigmoid()
            self.output_layer2 = network.layer(4, 2, self.weights[1])
            self.act_tanh = network.Activation_Tanh()
            self.weights = [self.hidden_layer1.weights, self.output_layer2.weights]
    class layer:
        def __init__(self, n_inputs, n_neurons, weights=None):
            if weights is None:
                self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
                #self.biases = np.zeros((1, n_neurons))
            else:
                self.weights = weights
                #self.biases = np.zeros((1, n_neurons))

        def forward(self, inputs):
            self.output = np.dot(inputs, self.weights)# + self.biases

    class Activation_Tanh:
        def forward(self, inputs):
            self.output = (np.exp(inputs) - np.exp(-inputs)) / \
                          (np.exp(inputs) + np.exp(-inputs))

    class Activation_Sigmoid:
        def forward(self, inputs):
            self.output = 1.0 / (1 + np.exp(-inputs))

    def runNN(self, sensors):
        sensor_input = np.concatenate((sensors, self.feedback))


        self.hidden_layer1.forward(sensor_input)

        self.act_sigmoid1.forward(self.hidden_layer1.output)
        hidden_layer_output = self.act_sigmoid1.output  # Also feedback
        self.feedback = hidden_layer_output


        self.output_layer2.forward(self.hidden_layer1.output)

        self.act_tanh.forward(self.output_layer2.output)
        motor_output = self.act_tanh.output
        return motor_output, hidden_layer_output
