from runRobot import RunRobot

iterations = 50

pop_size = 100
select_perc = 0.9
error_range = 0.1

runRobot = RunRobot(pop_size, select_perc, error_range)

runRobot.train(iterations)
