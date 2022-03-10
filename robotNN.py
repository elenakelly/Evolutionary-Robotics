import numpy as np
import random

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


        self.output_layer2.forward(self.act_sigmoid1.output)

        self.act_tanh.forward(self.output_layer2.output)
        motor_output = self.act_tanh.output
        return motor_output, hidden_layer_output

class RobotEA():
    def __init__(self, pop_size, select_perc, error_range, mutate):
        self.population = [Individual(network()) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
        self.mutate = mutate

    def selection(self):
        self.population.sort(key=lambda s: s.score, reverse=True)
        selected = self.population[:int(self.select_perc * (len(self.population)))]
        return selected

    def crossover(self, selected):
        children = []
        # create couples that will give birth
        parent_1 = [selected[rand] for rand in
                    np.random.randint(len(selected), size=int(self.pop_size))]
        parent_2 = [selected[rand] for rand in np.random.randint(len(selected), size=int(self.pop_size))]
        for i in range(int(self.pop_size)):
            # Crossover
            child = self.birth(parent_1[i], parent_2[i])
            children.append(child)
        return children

    def birth(self, parent_1,parent_2):
        weights = []
        for i in range(len(parent_1.dna)):
            # for every layer average
            weights.append(np.mean(np.array([parent_1.dna[i], parent_2.dna[i]]), axis=0))
        child = Individual(network(weights=weights))
        return child

    def mutation(self, children):
        for i in range(self.pop_size):
            if random.random() < self.mutate:
                weights = []
                #print("before mutation: ", children[i].dna)
                for j in range(len(children[i].dna)):
                    bias = np.random.uniform(-1,1, [children[i].dna[j].shape[0], children[i].dna[j].shape[1]])
                    bias = np.where(abs(bias) > 0.2, 0, bias * 0.1)
                    weights.append(children[i].dna[j] + bias)
                    #print("bias term", bias)
                children[i].dna = weights
                #print("after mutation: ", children[i].dna)
        return children

    def run(self):
        #life cycle

        selected = self.selection()
        #print("dna of first: ", selected[0].dna)
        children = self.crossover(selected)
        #print("dna of first after cross over: ", children[0].dna)
        children = self.mutation(children)
        #print("dna of first after mutation: ", children[0].dna)

        self.population = children

        return self.population

class Individual():
    def __init__(self, NN):
        self.NN = NN
        self.dna = NN.weights # float number
        self.score = 0

    def update_score(self, score):
        self.score = score

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Robot score: ' + str(self.score)


#Testing area
if __name__ == '__main__':
    pop_size = 100
    select_perc = 0.9
    error_range = 0.5
    epochs = 100

    robotEA = RobotEA(pop_size, select_perc, error_range)
    for epoch in range(epochs):
        robotEA.run()
