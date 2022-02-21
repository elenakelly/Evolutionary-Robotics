import functions
import plots
import EvolutionaryAlgorithms

global params
global func

#initialize
plot_range = [[-2, 2], [-2, 2]]
params = [1.,10.]
func = [functions.rosenbrock, [0, 10]]
#Hyperparameters initialization
pop_size = 99
function = [functions.rosenbrock, [0, 10]]
epochs = 100
selection_percentage = 0.95
error_range = [-0.15,0.15]


ea = EvolutionaryAlgorithms.EA(pop_size, selection_percentage, error_range, params)

filenames = []
for i in range(epochs):
    print("iteration: " + str(i))
    ea.run()
    filenames.append(plots.plotGraphs(ea.population, func, i, plot_range))
plots.createGif(filenames, name="EA.gif")

