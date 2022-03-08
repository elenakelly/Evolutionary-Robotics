from matplotlib import pyplot as plt
from robotNN import RobotEA
import ffnn
import pygame
import Robot

class RunRobot():
    def __init__(self, pop_size, select_perc, error_range):
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
    def train(self, epochs):
        robotEA = RobotEA(self.pop_size, self.select_perc, self.error_range)
        for epoch in range(epochs):
            for individual in robotEA.population:
                #create and simulate robot given the neural network
                individual.score = Robot.Robot(individual.NN)

                #print(individual.NN.weights)
            #call Evolutionary Algorithms to update the weights and proceed to the next iteration
            robotEA.run()
