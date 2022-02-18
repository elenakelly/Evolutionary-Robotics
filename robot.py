import pygame
from utils import blit_rotate_center
import random
import numpy as np
import math
import os

# os.chdir("C://Users/nickd/PycharmProjects/Mobile-Robot-Simulator")

# initialisation of game
pygame.font.init()

# images
BACKGROUND = pygame.image.load("images/background.png")
ROBOT = pygame.image.load("images/vacuum.png")
WALLTT = pygame.image.load("images/wallTT.png")
ICON = pygame.image.load('images/icon.png')

# main sceen
WIDTH, HEIGHT = 800, 600  # dimentions
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# window setting
pygame.display.set_caption("Mobile Robot Simulator")
pygame.display.set_icon(ICON)
pygame.rect.Rect
MAIN_FONT = pygame.font.SysFont("comicsans", 22)
SENSORS_FONT = pygame.font.SysFont("comicsans", 12)


# SENSORS - Divide circumference by number of sensors
STEP_ANGLE = (math.pi*2) / 12
# -------

# Robot movement


class RobotMove:
    def __init__(self):
        self.trail_set = []

        self.img = self.IMG  # image
        self.x = self.START_POS[0]  # starting x
        self.y = self.START_POS[1]  # starting y

        self.m2p = 3779.52  # meters to pixels
        self.vl = 0  # left velocity
        self.vr = 0  # right velocity
        self.theta = 0
        self.speed = 0.001
        distance = 64
        # distance between the centers of the two wheels
        self.l = int(distance/2)

        self.changeX = self.x + self.l
        self.changeY = self.y

        self.rect = pygame.Rect(self.x, self.y, 60, 60)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center =(self.x,self.y))
    

    # draw and rotate the image
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), math.degrees(self.theta))


    def move(self, keys, dt):

        # setting the buttons
        if keys[0] == 1:
            self.vl += self.speed
        if keys[1] == 1:
            self.vl -= self.speed
        if keys[2] == 1:
            self.vr += self.speed
        if keys[3] == 1:
            self.vr -= self.speed
        if keys[4] == 1:
            self.vl == self.vr
            self.vr += self.speed
            self.vl += self.speed
        if keys[5] == 1:
            self.vl == self.vr
            self.vr -= self.speed
            self.vl -= self.speed
        if keys[6] == 1:
            self.vl = 0
            self.vr = 0

          # check model
        if self.vr != 0 or self.vl != 0:
            if self.vl == self.vr:
                self.x += ((self.vl+self.vr)/2) * np.cos(self.theta) * dt
                self.y -= ((self.vl+self.vr)/2) * np.sin(self.theta) * dt
                R = np.inf
                w = 0
            else:
                R = self.l * (self.vl + self.vr) / (self.vr - self.vl)
                w = (self.vr - self.vl) / (self.l*2)

            # Computation of ICC
                ICC = [self.x - R * np.sin(-self.theta),
                       self.y + R * np.cos(self.theta)]
                rotation = np.transpose(np.matmul(
                    np.array([[np.cos(w * dt), -np.sin(w * dt), 0],
                              [np.sin(w * dt), np.cos(w * dt), 0],
                              [0, 0, 1]]),
                    np.transpose(np.array([self.x - ICC[0], self.y - ICC[1], self.theta]))) + np.array(
                    [ICC[0], ICC[1], w * dt])).transpose()

                u_col, b_col, r_col, l_col = self.is_colliding()
                print(u_col or b_col)
                if not (l_col or r_col):
                    self.x = rotation[0]
                if not (u_col or b_col):
                    self.y = rotation[1]
                self.theta = rotation[2]

        
        self.rotated =pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center = (self.x,self.y))

    def upd_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def is_colliding(self):
        uper_col = False
        bottom_col = False
        right_col = False
        left_col = False
        for wall in wall_list:
            if self.rect.colliderect(wall.rect):
                if abs(wall.rect.top - self.rect.bottom) < 10:
                    # print("upper col")
                    uper_col = True
                if abs(wall.rect.bottom - self.rect.top) < 10:
                    # print("bottom col")
                    bottom_col = True
                if abs(wall.rect.right - self.rect.left) < 10:
                    # print("right col")
                    right_col = True
                if abs(wall.rect.left - self.rect.right) < 10:
                    # print("left col")
                    left_col = True
        return uper_col, bottom_col, right_col, left_col





class PlayRobot(RobotMove):
    IMG = ROBOT
    START_POS = (random.uniform(40, 735), random.uniform(
        40, 535))  # start at random potition
    trail_set = []

    def collide(self):
        self.boundaryX = WIDTH - 64
        self.boundaryY = HEIGHT - 64
        # hit the wall
        if self.x <= 38:
            self.x = 38
        elif self.x >= self.boundaryX - 39:
            self.x = self.boundaryX - 39

        if self.y <= 38:
            self.y = 38
        elif self.y >= self.boundaryY - 39:
            self.y = self.boundaryY - 39


# Raycasting


def cast_rays(screen, walls):

    all_sensors = []

    sensor_x = player_robot.x+(ROBOT.get_width()/2)
    sensor_y = player_robot.y+(ROBOT.get_height()/2)

    temp_angle = 0
    for i in range(12):
        all_sensors.append((sensor_x, sensor_y, temp_angle, temp_angle, i))
        temp_angle += STEP_ANGLE

    for sensor in all_sensors:

        clipped_line = None

        for depth in range(200):
            target_x = sensor[0] - math.sin(sensor[2]) * depth
            target_y = sensor[1] + math.cos(sensor[3]) * depth

            ray = ((sensor_x, sensor_y), (target_x, target_y))

            for i in range(len(walls)):
                clipped_line = walls[i].clipline(ray)
                if clipped_line:
                    break

        sensor_placement_offset = 8
        sensor_placement_radius_depth = 64
        sensor_placement_x = sensor[0] - math.sin(
            sensor[2]) * sensor_placement_radius_depth - sensor_placement_offset
        sensor_placement_y = sensor[1] + math.cos(
            sensor[3]) * sensor_placement_radius_depth - sensor_placement_offset
        collision_offset = 29
        if clipped_line:
            sensor_distance = int(
                math.sqrt((clipped_line[0][1]-sensor_y)**2 + (clipped_line[0][0]-sensor_x)**2))-collision_offset
        else:
            sensor_distance = 200

        sensor_text = SENSORS_FONT.render(
            f"{sensor_distance}", 1, (255, 255, 255))
        screen.blit(
            sensor_text, (sensor_placement_x, sensor_placement_y))

    # ------------

'''
def wall_collision(robot, screen, WallRect):

    offset_x = WallRect.x - robot.x
    offset_y = WallRect.y - robot.y
    robot_mask = pygame.mask.from_surface(robot.img)
    wall_mask = pygame.mask.from_surface(WALLTT)
    col_mask = robot_mask.overlap(wall_mask, (offset_x, offset_y))
    if col_mask:
        print("COLLISION")
        col_text = MAIN_FONT.render(
            f"COLLISION", 1, (255, 255, 255))
        screen.blit(col_text, (530, 140))
        pygame.display.flip()
    return col_mask, offset_x, offset_y

'''

# setting the enviroment


class Envir:
    def __init__(self, dimention):
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        # map_dims
        self.height = dimention[0]
        self.width = dimention[1]
        # window setting
        self.map = pygame.display.set_mode((self.width, self.height))
        # trail
        self.trail_set = []
    # line route

    def trail(self, pos):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(self.map, self.white, (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__() > 10000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)
    # y and x axis

    def robot_frame(self, pos, rotation):
        n = 80
        centerx, centery = pos
        x_axis = (centerx + n*np.cos(-rotation), centery + n*np.sin(-rotation))
        y_axis = (centerx + n*np.cos(-rotation+np.pi/2),
                  centery + n*np.sin(-rotation+np.pi/2))
        pygame.draw.line(self.map, self.black, (centerx, centery), x_axis, 3)
        pygame.draw.line(self.map, self.black, (centerx, centery), y_axis, 3)

    def draw(self, screen, images, player_robot):

        # display images on screen
        for img, pos in images:
            screen.blit(img, pos)

        # display left, right velocity and theta on screen
        vel_text = MAIN_FONT.render(
            f"Vl = {round(player_robot.vl,2)} Vr = {round(player_robot.vr,2)} theta = {int(np.degrees(player_robot.theta))}", 1, self.white)
        screen.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 40))

        # display robot on screen
        player_robot.draw(screen)
        # pygame.display.update()

    def setWalls():
        wall_pixel_offset = 42
        rectWallL = pygame.Rect(0, 0, wall_pixel_offset, HEIGHT)
        rectWallR = pygame.Rect(WIDTH-wall_pixel_offset, 0,
                                wall_pixel_offset, HEIGHT)
        rectWallT = pygame.Rect(0,  0, WIDTH, wall_pixel_offset)
        rectWallB = pygame.Rect(0, HEIGHT-wall_pixel_offset,
                                WIDTH, wall_pixel_offset)
        return [rectWallL, rectWallR, rectWallT, rectWallB]


class Wall():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 51, 0), self.rect)


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
