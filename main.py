import random
import numpy as np
import functions
import plots

global params
global func  #TODO change these
global plot_range
plot_range = [[-2, 2], [-2, 2]]
params = [1.,10.]
func = [functions.rosenbrock, [0, 10]]

class EA:
    def __init__(self, pop_size):
        self.bit_string_len = 8
        self.population = [Strumf([np.random.randint(-10,10),np.random.randint(-10, 10)]) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.bounds = [[-10,10],[-10,10]]

        #self.evaluations = self.evaluate()

    def evaluate(self):
        return [strumf.evaluate() for strumf in self.population]

    def selection(self, n=50):
        pass
        #self.evaluations

    def crossover(self, parent_1,parent_2):
        child_1 = Strumf([parent_1.dna[0], parent_2.dna[1]])
        child_2 = Strumf([parent_1.dna[1], parent_2.dna[0]])
        return child_1, child_2

    def run(self):
        scores = self.evaluate()

        #print(self.population)
        #[strumf.decode(self.bounds, self.bit_string_len) for strumf in self.population]
        self.population.sort(key=lambda s:s.score)
        selected = self.population[:3]

        descendant = []
        np.random.randint(2, size=10)

        #create couples that will give birth
        parent_1 = [selected[rand] for rand in np.random.randint(len(selected), size=int(self.pop_size/2))] #TODO check if ODD or EVEN
        parent_2 = [selected[rand] for rand in np.random.randint(len(selected), size=int(self.pop_size/2))]
        for i in range(int(self.pop_size/2)):
            #Crossover
            child_1, child_2 = self.crossover(parent_1[i], parent_2[i]) #TODO it can be coupled with it self as well

            #max(0, min(new_index, len(mylist)-1))

            descendant.append(child_1)
            descendant.append(child_2)

        # Mutation
        for i in range(self.pop_size):
            if random.random() > 0.8: # TODO we can play with the probability
                self.population[i].dna[0] = max(-5, min(self.population[i].dna[0] + np.random.randint(-10, 10),5))  # TODO change range of number
                self.population[i].dna[1] = max(-5, min(self.population[i].dna[1] + np.random.randint(-10, 10), 5))
        #print(self.population)


class Strumf():
    def __init__(self, dna):
        self.dna = dna # 2D space # is the DNA information in bit format(e.x. 10001101010) #TODO change this to real values
        self.score = func[0](self.dna, params)

    def evaluate(self):
        self.score = func[0](self.dna, params)
        return func[0](self.dna, params)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Strumf DNA: " + str(self.dna) + " and loss: " + str(self.evaluate())

    '''def decode(self, bounds):
        print(bounds[0][0] + (self.dna[0]/255) * (bounds[0][1] - bounds[0][0]))
        decoded = [bounds[0][0] + (self.dna[0]/255)(bounds[0][1] - bounds[0][0]), bounds[0][0] + (self.dna[1]/255) * (bounds[0][1] - bounds[0][0])]
        print(decoded)
        return decoded
    def encode(self, bounds, bit_string_len):
        x_scaled(round(self.dna))
        print('{:0{}b}'.format(x_scaled, bit_string_len))
        pass'''

if __name__ == "__main__":
    filenames = []

    ea = EA(100)
    for i in range(100):
        ea.run()
        filenames.append(plots.plotGraphs(ea.population, func, i, plot_range))
    plots.createGif(filenames, name="EA.gif")
    #print(ea.population[0].dna)
    #print(ea.evaluations)

