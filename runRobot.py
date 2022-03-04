
from matplotlib import pyplot as plt
from robotNN import  RobotNN, RobotEA


def plot():
    #Show evolution of fitness (max + average)
    plt.title("Minimum evaluations per iteration")
    plt.show()

    plt.title("Average evaluations per iteration")
    plt.show()

def train(iterations):
    #call robotNN & robotEA and train it 
    pass



if __name__ == "__main__":
    iterations = 50
    train(iterations)