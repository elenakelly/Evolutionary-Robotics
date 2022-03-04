
from matplotlib import pyplot as plt


def plot():
    #Show evolution of fitness (max + average)
    plt.title("Minimum evaluations per iteration")
    plt.show()

    plt.title("Average evaluations per iteration")
    plt.show()

def train(iterations):
    pass

def display_result(iterations):
    pass


if __name__ == "__main__":
    iterations = 50
    train(iterations)
    display_result(iterations)