from matplotlib import pyplot as plt
from robotNN import RobotNN, RobotEA
import pygame
import robot

'''# initialisation of game
pygame.font.init()

# images
BACKGROUND = pygame.image.load("images/background.png")
# main sceen
WIDTH, HEIGHT = 800, 600  # dimentions
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# running game or not
run = True

images = [(BACKGROUND, (0, 0))]
# the robot
player_robot = PlayRobot()



# walls
wall_list = [Wall(100, 200, 300, 10), Wall(
    100, 200, 10, 300), Wall(400, 10, 10, 300)]

# enviroment prints
enviroment = Envir([600, 800])
walls = Envir.setWalls()

for wall in wall_list:
    walls.append(wall.rect)

# Test Wall
# WallTTRect = pygame.Rect(542, 142, WALLTT.get_width(), WALLTT.get_height())
# walls.append(WallTTRect)
# ----

# dt
dt = 50
clock = pygame.time.Clock()
FPS = 60




# simulation loop
while run:

    # activate quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # timer
    clock.tick(FPS)

    # activate buttons
    keys = pygame.key.get_pressed()
    key = [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_o], keys[pygame.K_l],
           keys[pygame.K_t], keys[pygame.K_g], keys[pygame.K_x]]

    # run the robot
    activate = player_robot.move(key, dt)
    player_robot.collide()

    # visualize objects

    # wall_collision(player_robot, SCREEN, WallRect)
    enviroment.draw(SCREEN, images, player_robot)
    for wall in wall_list:
        wall.draw(SCREEN)
    enviroment.robot_frame(
        (player_robot.x, player_robot.y), player_robot.theta)
    enviroment.trail((player_robot.x, player_robot.y))
    player_robot.draw(enviroment.map)
    player_robot.upd_rect()
    cast_rays(SCREEN, walls)

    # ---

    pygame.display.update()

# exit the game
pygame.quit()


def plot():
    #Show evolution of fitness (max + average)
    plt.title("Minimum evaluations per iteration")
    plt.show()

    plt.title("Average evaluations per iteration")
    plt.show()
'''
neural_network = RobotNN()
[vl,vr] = RobotNN.forward_propagate()

def train(iterations):



    pop_size = 100
    select_perc = 0.9
    error_range = 0.5
    epochs = 100

    robotEA = RobotEA(pop_size, select_perc, error_range)
    for epoch in range(epochs):
        for individual in robotEA.population:
            weights = individual.dna

            # TODO call robotNN to compute the movement vector

            # TODO run simulation
            score = None

            individual.score = score

            #so now we have all robots scores updated given the NN output(fed with weights)

if __name__ == "__main__":
    iterations = 50
    train(iterations)