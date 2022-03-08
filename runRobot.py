from matplotlib import pyplot as plt
from robotNN import RobotEA
import ffnn
import pygame
import Robot
import matplotlib.pyplot as plt
class RunRobot():
    def __init__(self, pop_size, select_perc, error_range):
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
    def train(self, epochs):
        robotEA = RobotEA(self.pop_size, self.select_perc, self.error_range)
        average_scores = []
        best_scores = []
        for epoch in range(epochs):
            accumulated_score = 0

            for individual in robotEA.population:
                #create and simulate robot given the neural network
                individual.score = Robot.Robot(individual.NN).results
                #print("score: ", individual.score)
                accumulated_score +=individual.score
                print(individual.score)
            average_scores.append(accumulated_score/len(robotEA.population))

            print("Iteration ", epoch, " score: ", accumulated_score/len(robotEA.population))
            #call Evolutionary Algorithms to update the weights and proceed to the next iteration
            robotEA.run()
            best_scores.append(robotEA.population[0].score)
        print(average_scores)
        plt.plot(average_scores, label="Average Scores")
        plt.plot(best_scores, label="Best Scores")
        plt.show()
