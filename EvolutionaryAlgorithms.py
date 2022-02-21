import random
import numpy as np
import functions



class EA():
    parms = None
    def __init__(self, pop_size, sel_perc, error_range, params, func):
        self.param = params
        self.func = func
        self.population = [Individual([np.random.uniform(-2,2),np.random.uniform(-2, 2)], self.param, self.func) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.sel_perc = sel_perc
        self.error_range = error_range


    def evaluate(self):
        return [individual.evaluate(self.param, self.func) for individual in self.population]

    def selection(self):
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
            child = self.birth(parent_1[i], parent_2[i])

            # max(0, min(new_index, len(mylist)-1))

            children.append(child)
        return children

    def birth(self, parent_1,parent_2):
        child = Individual([np.mean([parent_1.dna[0], parent_2.dna[0]]), np.mean([parent_1.dna[1], parent_2.dna[1]])], self.param,self.func)
        return child

    def mutation(self, children):
        j=0
        for i in range(self.pop_size):

            if random.random() > self.sel_perc :
                j +=1
                children[i].dna[0] = max(-5, min(children[i].dna[0] + np.random.uniform(self.error_range[0], self.error_range[1]),5))
                children[i].dna[1] = max(-5, min(children[i].dna[1] + np.random.uniform(self.error_range[0], self.error_range[1]), 5))

        return children

    def run(self):

        #life cycle
        selected = self.selection()
        children = self.crossover(selected)
        children = self.mutation(children)
        self.population = children


class Individual():
    def __init__(self, dna, param, func):
        self.func = func
        self.param = param
        self.dna = dna # float number
        self.score = func[0](self.dna, param)

    def evaluate(self, parm, func):
        self.score = func[0](self.dna, parm)
        return func[0](self.dna, parm)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "individual DNA: " + str(self.dna) + " and loss: " + str(self.evaluate(self.param, self.func))