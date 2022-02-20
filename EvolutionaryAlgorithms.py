import random
import numpy as np
import functions
import plots

#graph parameters initialization
plot_range = [[-2, 2], [-2, 2]]
params = [1.,10.]
func = [functions.rosenbrock, [0, 10]]

class EA():
    def __init__(self, pop_size, sel_perc, error_range):
        self.population = [Strumf([np.random.uniform(-2,2),np.random.uniform(-2, 2)]) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.sel_perc = sel_perc
        self.error_range = error_range

    def evaluate(self):
        return [strumf.evaluate() for strumf in self.population]

    def selection(self, n=50):
        self.population.sort(key=lambda s: s.score)
        selected = self.population[:int(self.sel_perc * (len(self.population)))]
        return selected

    def crossover(self, selected):
        children = []

        # create couples that will give birth
        parent_1 = [selected[rand] for rand in
                    np.random.randint(len(selected), size=int(self.pop_size))]
        parent_2 = [selected[rand] for rand in np.random.randint(len(selected), size=int(self.pop_size))]
        for i in range(int(self.pop_size)):
            # Crossover
            child = self.birth(parent_1[i], parent_2[i])  # TODO it can be coupled with it self as well

            # max(0, min(new_index, len(mylist)-1))

            children.append(child)
        return children

    def birth(self, parent_1,parent_2):
        child = Strumf([np.mean([parent_1.dna[0], parent_2.dna[0]]), np.mean([parent_1.dna[1], parent_2.dna[1]])])
        return child

    def mutation(self, children):
        for i in range(self.pop_size):
            if random.random() > self.sel_perc :
                self.population[i].dna[0] = max(-5, min(children[i].dna[0] + np.random.uniform(self.error_range[0], self.error_range[1]),5))  # TODO change range of number
                self.population[i].dna[1] = max(-5, min(children[i].dna[1] + np.random.uniform(self.error_range[0], self.error_range[1]), 5))

    def run(self):
        print(self.population)

        #life cycle
        selected = self.selection()
        children = self.crossover(selected)
        self.mutation(children)

class Strumf():
    def __init__(self, dna):
        self.dna = dna # float number
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
