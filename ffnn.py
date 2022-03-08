import numpy as np


class network():
    def __init__(self):

        self.feedback = [0, 0, 0, 0]

    def runNN(self, sensors):

        class layer:
            def __init__(self, n_inputs, n_neurons):
                self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
                self.biases = np.zeros((1, n_neurons))

            def forward(self, inputs):
                self.output = np.dot(inputs, self.weights) + self.biases

        class Activation_Tanh:
            def forward(self, inputs):
                self.output = (np.exp(inputs) - np.exp(-inputs)) / \
                    (np.exp(inputs) + np.exp(-inputs))

        class Activation_Sigmoid:
            def forward(self, inputs):
                self.output = 1.0/(1+np.exp(-inputs))

        sensor_input = sensors + self.feedback

        hidden_layer = layer(16, 4)
        hidden_layer.forward(sensor_input)

        act_sigmoid = Activation_Sigmoid()
        act_sigmoid.forward(hidden_layer.output)
        hidden_layer_output = act_sigmoid.output  # Also feedback
        self.feedback = hidden_layer_output

        output_layer = layer(4, 2)
        output_layer.forward(hidden_layer.output)
        act_tanh = Activation_Tanh()
        act_tanh.forward(output_layer.output)
        motor_output = act_tanh.output

        return motor_output, hidden_layer_output
