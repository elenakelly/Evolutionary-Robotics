#import robot
import numpy as np
import random

class RobotNN():
    def __init__(self, *args):
        if len(args) <= 1:
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

            # create activations
            activations = []
            for i in range(len(layers)):
                a = np.zeros(layers[i])
                activations.append(a)
            self.activations = activations

        elif len(args) > 1:
            pass


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
    def __init__(self, pop_size, select_perc, error_range):
        self.population = [Individual(RobotNN()) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range


    def evaluate(self):
        return [individual.evaluate() for individual in self.population]

    def selection(self):
        self.population.sort(key=lambda s: s.score)
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
            weights.append(np.mean(np.array([parent_1.dna[i], parent_2.dna[i]]), axis=0))
        child = Individual(RobotNN(weights))
        return child

    def mutation(self, children):
        for i in range(self.pop_size):
            if random.random() > self.select_perc:
                # TODO change how noise is added(what we do now is we create a random matrix and add it)
                weights = []
                for j in range(len(children[i].dna)):
                    weights.append(children[i].dna[j] + (0.001 * np.random.rand(*children[i].dna[j].shape)))
                children[i].dna = weights
        return children

    def run(self):
        #life cycle
        selected = self.selection()
        children = self.crossover(selected)
        children = self.mutation(children)
        self.population = children

        return self.population

class Individual():
    def __init__(self, robot):
        self.dna = robot.weights # float number
        self.score = 0

    def evaluate(self, score):
        # TODO evaluation function goes here
        self.score = score

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Robot score: ' + self.score


#Testing area
if __name__ == '__main__':
    pop_size = 100
    select_perc = 0.9
    error_range = 0.5
    epochs = 100

    robotEA = RobotEA(pop_size, select_perc, error_range)
    for epoch in range(epochs):
        robotEA.run()
