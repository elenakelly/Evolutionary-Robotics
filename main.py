import functions
from EA import EA

if __name__ == "__main__":
    
    # Objective Function and the parameters it takes
    #function = [functions.rosenbrock, [0, 10]]
    function = [functions.rastrigin, [10]]

    # Plot Range
    plot_range = [[-10000, 10000], [-10000, 10000]]  # Better for Rastrigin
    # plot_range = [[-2, 2], [-1, 3]]  # Better for Rosenbrock

    # Run EA
    EA()