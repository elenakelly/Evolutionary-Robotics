from runRobot import RunRobot

iterations = 100

pop_size = 15
select_perc = 0.5
error_range = 0.1
mutate = 0.5

runRobot = RunRobot(pop_size, select_perc, error_range, mutate)

runRobot.train(iterations)
