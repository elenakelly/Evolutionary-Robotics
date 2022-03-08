from runRobot import RunRobot

iterations = 10

pop_size = 5
select_perc = 0.9
error_range = 0.1

runRobot = RunRobot(pop_size, select_perc, error_range)

runRobot.train(iterations)
