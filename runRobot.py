from matplotlib import pyplot as plt
from robotNN import RobotEA
import Robot
import matplotlib.pyplot as plt

class RunRobot():
    def __init__(self, pop_size, select_perc, error_range, mutate):
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
        self.mutate = mutate
        self.robotEA = RobotEA(self.pop_size, self.select_perc, self.error_range, self.mutate)
    def train(self, epochs):
        average_scores = []
        best_scores = []
        for epoch in range(epochs):
            accumulated_score = 0
            print("=============start of epoch=====================")
            for i in range(len(self.robotEA.population)):
                #create and simulate robot given the neural network
                self.robotEA.population[i].update_score(Robot.Robot(self.robotEA.population[i].NN, epoch, i).results)
                print("this is the score returned from the simulation", self.robotEA.population[i].score)
                accumulated_score +=self.robotEA.population[i].score

            average_scores.append(accumulated_score/len(self.robotEA.population))

            lis = [rob.score for rob in self.robotEA.population]
            lis.sort()
            print("Iteration ", epoch, " best score: ", [rob.score for rob in self.robotEA.population])
            print("Iteration ", epoch, " best score: ", max(lis))
            best_scores.append(max(lis))

            # call Evolutionary Algorithms to update the weights and proceed to the next iteration
            self.robotEA.run()
            print("=============end of epoch=====================")
        plt.plot(average_scores, label="Average Scores", c='blue')
        plt.plot(best_scores, label="Best Scores", c='red')
        plt.show()
