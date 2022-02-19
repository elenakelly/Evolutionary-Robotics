import numpy as np

# Rosenbrock Function
# x[0] is the x-coordinate and x[1] is the y-coordinate of the function
# parameters[0] is the a and parameter[1] is the b of the function


def rosenbrock(x, parameters):
    return ((parameters[0] - x[0]) ** 2) + parameters[1]*((x[1]-(x[0]**2))**2)


# Rastrigin Function
# x is a list of the dimensions of the function
# parameters[0] is the A of the function
def rastrigin(x, parameters):

    # Calculate n (n is the dimensionality of the function)
    n = len(x)

    # Add n multiplied by A to the running total
    total = parameters[0]*n

    # Add the sum part of each dimension of the function to the running total
    for i in range(n):
        total = total + (x[i]**2 - parameters[0] * np.cos(2*np.pi * x[i]))

    return total