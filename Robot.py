import pygame
import random
import numpy as np
import math
import os

# os.chdir("C://Users/nickd/PycharmProjects/Mobile-Robot-Simulator")
# os.environ["SDL_VIDEODRIVER"] = "dummy"


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))

# Robot movement


class RobotMove:
    def __init__(self, IMG):
        self.trail_set = []

        self.img = IMG  # image
        self.x = self.START_POS[0]  # starting x
        self.y = self.START_POS[1]  # starting y

        self.m2p = 3779.52  # meters to pixels
        self.vl = 0  # left velocity
        self.vr = 0  # right velocity
        self.theta = 0
        self.speed = 0.001
        distance = 64
        # distance between the centers of the two wheels
        self.l = int(IMG.get_width())

        self.changeX = self.x + (self.l/2)
        self.changeY = self.y

        self.rect = pygame.Rect(
            self.x, self.y, IMG.get_width(), IMG.get_height())
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
        self.dustCleared = 0
        self.wallCollisions = 0
        self.hasCollided = False

    # draw and rotate the image

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y),
                           math.degrees(-self.theta))

    def simulation_move(self, vl, vr, dt, wall_list, screen):

        self.vl = vl
        self.vr = vr
        next_x, next_y = self.x, self.y

        # check model
        if self.vr != 0 or self.vl != 0:
            if self.vl == self.vr:
                next_x = self.x + ((self.vl+self.vr)/2) * \
                    np.cos(-self.theta) * dt
                next_y = self.y - ((self.vl+self.vr)/2) * \
                    np.sin(-self.theta) * dt
                R = np.inf
                w = 0
            else:
                R = (self.l/2) * (self.vl + self.vr) / (self.vr - self.vl)
                w = (self.vr - self.vl) / self.l

            # Computation of ICC

                centerx = self.x+(self.img.get_width()/2)
                centery = self.y+(self.img.get_height()/2)
                ICC = [centerx - R * np.sin(self.theta),
                       centery + R * np.cos(self.theta)]

                a = [[np.cos(w * dt), -np.sin(w * dt), 0],
                     [np.sin(w * dt), np.cos(w * dt), 0], [0, 0, 1]]
                b = [centerx - ICC[0], centery - ICC[1], self.theta]
                rotation = np.dot(a, b)
                rotation = rotation + [ICC[0], ICC[1], w * dt]

                pygame.draw.line(screen, (255, 255, 0), (centerx, centery),
                                 (ICC[0], ICC[1]), 3)
                pygame.display.flip()

                next_x = rotation[0]-(self.img.get_width()/2)
                next_y = rotation[1]-(self.img.get_height()/2)
                self.theta = rotation[2]

        self.rotated = pygame.transform.rotozoom(
            self.img, math.degrees(self.theta), 1)
        # self.rect = self.rotated.get_rect(center=(self.x, self.y))

        self.collide2((self.x, self.y), (next_x, next_y), wall_list)
        # self.collide((self.x, self.y), (next_x, next_y),width,height)

    def move(self, keys, dt, wall_list, screen):

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

        next_x, next_y = self.x, self.y

        # check model
        if self.vr != 0 or self.vl != 0:
            if self.vl == self.vr:
                next_x = self.x + ((self.vl+self.vr)/2) * \
                    np.cos(-self.theta) * dt
                next_y = self.y - ((self.vl+self.vr)/2) * \
                    np.sin(-self.theta) * dt
                R = np.inf
                w = 0
            else:
                R = (self.l/2) * (self.vl + self.vr) / (self.vr - self.vl)
                w = (self.vr - self.vl) / self.l

            # Computation of ICC

                centerx = self.x+(self.img.get_width()/2)
                centery = self.y+(self.img.get_height()/2)
                ICC = [centerx - R * np.sin(self.theta),
                       centery + R * np.cos(self.theta)]

                a = [[np.cos(w * dt), -np.sin(w * dt), 0],
                     [np.sin(w * dt), np.cos(w * dt), 0], [0, 0, 1]]
                b = [centerx - ICC[0], centery - ICC[1], self.theta]
                rotation = np.dot(a, b)
                rotation = rotation + [ICC[0], ICC[1], w * dt]

                pygame.draw.line(screen, (255, 255, 0), (centerx, centery),
                                 (ICC[0], ICC[1]), 3)
                pygame.display.flip()

                next_x = rotation[0]-(self.img.get_width()/2)
                next_y = rotation[1]-(self.img.get_height()/2)
                self.theta = rotation[2]

        self.rotated = pygame.transform.rotozoom(
            self.img, math.degrees(self.theta), 1)
        # self.rect = self.rotated.get_rect(center=(self.x, self.y))

        self.collide2((self.x, self.y), (next_x, next_y), wall_list)
        # self.collide((self.x, self.y), (next_x, next_y),width,height)

    def upd_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def is_colliding(self, cur_pos, next_pos, wall_list):
        uper_col = [False, 0]
        bottom_col = [False, 0]
        right_col = [False, 0]
        left_col = [False, 0]

        temp_new = next_pos
        print(cur_pos[0])
        if cur_pos[0] > 695:
            print("cur x", cur_pos[0])

        if cur_pos[1] < 40:
            print("cur y", cur_pos[0])

        detected = []
        detected_x = []
        detected_y = []

        # if abs(cur_pos[0] - temp_new[0]) > 10 or abs(cur_pos[1] - temp_new[1]) > 10:

        incremented_x = cur_pos[0]
        incremented_y = cur_pos[1]

        # if cur_pos[0] != temp_new[0] and cur_pos[1] != temp_new[1]:
        # MOVING LEFT UP
        if cur_pos[0] >= temp_new[0] and cur_pos[1] > temp_new[1]:

            searching = [True, True]
            switch_increment = True  # True increments x

            while searching[0] == True or searching[1] == True:

                next_rect = pygame.Rect(
                    incremented_x, incremented_y, self.img.get_width(), self.img.get_height())

                for wall in wall_list:
                    if next_rect.colliderect(wall.rect):

                        if abs(wall.rect.top - next_rect.bottom) <= 10:
                            # print("upper col")
                            uper_col[0] = True
                            uper_col[1] = wall.rect.top - \
                                self.img.get_height()
                        elif abs(wall.rect.bottom - next_rect.top) <= 10:
                            # print("bottom col")
                            bottom_col[0] = True
                            bottom_col[1] = wall.rect.bottom

                        if abs(wall.rect.right - next_rect.left) <= 10:
                            # print("right col")
                            right_col[0] = True
                            right_col[1] = wall.rect.right
                        elif abs(wall.rect.left - next_rect.right) <= 10:
                            # print("left col")
                            left_col[0] = True
                            left_col[1] = wall.rect.left - \
                                self.img.get_width()

                        # if not (uper_col[0] or bottom_col[0] or right_col[0] or left_col[0]):
                        #     if switch_increment:
                        #         bottom_col[0] = True
                        #         bottom_col[1] = wall.rect.bottom
                        #     else:
                        #         right_col[0] = True
                        #         right_col[1] = wall.rect.right

                if incremented_x <= temp_new[0] or right_col[0] or left_col[0]:
                    searching[0] = False
                if incremented_y <= temp_new[1] or uper_col[0] or bottom_col[0]:
                    searching[1] = False

                if bottom_col[0] and right_col[0]:
                    return uper_col, bottom_col, right_col, left_col

                if bottom_col[0] and searching[0] == False:
                    return uper_col, bottom_col, right_col, left_col

                if right_col[0] and searching[1] == False:
                    return uper_col, bottom_col, right_col, left_col

                if switch_increment:
                    if searching[0]:
                        incremented_x = incremented_x - 1
                    switch_increment = not switch_increment
                else:
                    if searching[1]:
                        incremented_y = incremented_y - 1
                    switch_increment = not switch_increment

        # MOVING RIGHT BOTTOM
        elif cur_pos[0] < temp_new[0] and cur_pos[1] <= temp_new[1]:

            searching = [True, True]
            switch_increment = True  # True increments x

            while searching[0] == True or searching[1] == True:

                next_rect = pygame.Rect(
                    incremented_x, incremented_y, self.img.get_width(), self.img.get_height())

                for wall in wall_list:
                    if next_rect.colliderect(wall.rect):

                        if abs(wall.rect.top - next_rect.bottom) <= 10:
                            # print("upper col")
                            uper_col[0] = True
                            uper_col[1] = wall.rect.top - \
                                self.img.get_height()
                        elif abs(wall.rect.bottom - next_rect.top) <= 10:
                            # print("bottom col")
                            bottom_col[0] = True
                            bottom_col[1] = wall.rect.bottom

                        if abs(wall.rect.right - next_rect.left) <= 10:
                            # print("right col")
                            right_col[0] = True
                            right_col[1] = wall.rect.right
                        elif abs(wall.rect.left - next_rect.right) <= 10:
                            # print("left col")
                            left_col[0] = True
                            left_col[1] = wall.rect.left - \
                                self.img.get_width()

                        # if switch_increment:
                        #     uper_col[0] = True
                        #     uper_col[1] = wall.rect.top - \
                        #         ROBOT.get_height()
                        # else:
                        #     left_col[0] = True
                        #     left_col[1] = wall.rect.left - \
                        #         ROBOT.get_width()

                if incremented_x >= temp_new[0] or right_col[0] or left_col[0]:
                    searching[0] = False
                if incremented_y >= temp_new[1] or uper_col[0] or bottom_col[0]:
                    searching[1] = False

                if uper_col[0] and left_col[0]:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])

                    return uper_col, bottom_col, right_col, left_col

                if uper_col[0] and searching[0] == False:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])

                    return uper_col, bottom_col, right_col, left_col
                if left_col[0] and searching[1] == False:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])

                    return uper_col, bottom_col, right_col, left_col

                if switch_increment:
                    if searching[0]:
                        incremented_x = incremented_x + 1
                    switch_increment = not switch_increment
                else:
                    if searching[1]:
                        incremented_y = incremented_y + 1
                    switch_increment = not switch_increment

        # MOVE LEFT BOTTOM
        elif cur_pos[0] >= temp_new[0] and cur_pos[1] <= temp_new[1]:

            searching = [True, True]
            switch_increment = True  # True increments x

            while searching[0] == True or searching[1] == True:

                next_rect = pygame.Rect(
                    incremented_x, incremented_y, self.img.get_width(), self.img.get_height())

                for wall in wall_list:
                    if next_rect.colliderect(wall.rect):

                        if abs(wall.rect.top - next_rect.bottom) <= 10:
                            # print("upper col")
                            uper_col[0] = True
                            uper_col[1] = wall.rect.top - \
                                self.img.get_height()
                        elif abs(wall.rect.bottom - next_rect.top) <= 10:
                            # print("bottom col")
                            bottom_col[0] = True
                            bottom_col[1] = wall.rect.bottom

                        if abs(wall.rect.right - next_rect.left) <= 10:
                            # print("right col")
                            right_col[0] = True
                            right_col[1] = wall.rect.right
                        elif abs(wall.rect.left - next_rect.right) <= 10:
                            # print("left col")
                            left_col[0] = True
                            left_col[1] = wall.rect.left - \
                                self.img.get_width()

                        # if switch_increment:
                        #     uper_col[0] = True
                        #     uper_col[1] = wall.rect.top - \
                        #         ROBOT.get_height()
                        # else:
                        #     left_col[0] = True
                        #     left_col[1] = wall.rect.left - \
                        #         ROBOT.get_width()

                if incremented_x <= temp_new[0] or left_col[0] or right_col[0]:
                    searching[0] = False
                if incremented_y >= temp_new[1] or uper_col[0] or bottom_col[0]:
                    searching[1] = False

                if uper_col[0] and left_col[0]:
                    return uper_col, bottom_col, right_col, left_col

                if uper_col[0] and searching[0] == False:
                    return uper_col, bottom_col, right_col, left_col
                if left_col[0] and searching[1] == False:
                    return uper_col, bottom_col, right_col, left_col

                if switch_increment:
                    if searching[0]:
                        incremented_x = incremented_x - 1
                    switch_increment = not switch_increment
                else:
                    if searching[1]:
                        incremented_y = incremented_y + 1
                    switch_increment = not switch_increment

        # MOVE RIGHT UP
        elif cur_pos[0] < temp_new[0] and cur_pos[1] > temp_new[1]:

            searching = [True, True]
            switch_increment = True  # True increments x

            while searching[0] == True or searching[1] == True:

                next_rect = pygame.Rect(
                    incremented_x, incremented_y, self.img.get_width(), self.img.get_height())

                for wall in wall_list:
                    if next_rect.colliderect(wall.rect):

                        if abs(wall.rect.top - next_rect.bottom) <= 10:
                            # print("upper col")
                            uper_col[0] = True
                            uper_col[1] = wall.rect.top - \
                                self.img.get_height()
                        elif abs(wall.rect.bottom - next_rect.top) <= 10:
                            # print("bottom col")
                            bottom_col[0] = True
                            bottom_col[1] = wall.rect.bottom

                        if abs(wall.rect.right - next_rect.left) <= 10:
                            # print("right col")
                            right_col[0] = True
                            right_col[1] = wall.rect.right
                        elif abs(wall.rect.left - next_rect.right) <= 10:
                            # print("left col")
                            left_col[0] = True
                            left_col[1] = wall.rect.left - \
                                self.img.get_width()

                        # if switch_increment:
                        #     bottom_col[0] = True
                        #     bottom_col[1] = wall.rect.bottom
                        # else:
                        #     left_col[0] = True
                        #     left_col[1] = wall.rect.left - \
                        #         ROBOT.get_width()

                if incremented_x >= temp_new[0] or left_col[0] or right_col[0]:
                    searching[0] = False
                if incremented_y <= temp_new[1] or uper_col[0] or bottom_col[0]:
                    searching[1] = False

                if bottom_col[0] and left_col[0]:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])
                    return uper_col, bottom_col, right_col, left_col

                if bottom_col[0] and searching[0] == False:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])

                    return uper_col, bottom_col, right_col, left_col
                if left_col[0] and searching[1] == False:

                    if bottom_col[1] < 40:
                        print("cur x", bottom_col[1])

                    if left_col[1]+self.img.get_width() > 695:
                        print("cur x", left_col[1])

                    return uper_col, bottom_col, right_col, left_col

                if switch_increment:
                    if searching[0]:
                        incremented_x = incremented_x + 1
                    switch_increment = not switch_increment
                else:
                    if searching[1]:
                        incremented_y = incremented_y - 1
                    switch_increment = not switch_increment

                # for wall in wall_list:

                #     if abs(cur_pos[0] - temp_new[0]) > 15 or abs(cur_pos[1] - temp_new[1]) > 15:
                #         # pygame.draw.line(SCREEN, (255, 255, 0), (cur_pos[0], cur_pos[1]),
                #         #                  (next_pos[0], next_pos[1]), 3)
                #         # pygame.display.flip()

                #         # dif_range = int(abs(cur_pos[0] - next_pos[0]))

                #         ray = (cur_pos[0], cur_pos[1]), (temp_new[0], temp_new[1])
                #         ray_x = (cur_pos[0], cur_pos[1]), (cur_pos[0], temp_new[1])
                #         ray_y = (cur_pos[0], cur_pos[1]), (temp_new[0], cur_pos[1])

                #         clipped_line = wall.rect.clipline(ray)
                #         if clipped_line:
                #             # detected.append(clipped_line)
                #             pygame.draw.line(SCREEN, (43, 43, 14), (clipped_line[0][0], clipped_line[0][1]),
                #                              (clipped_line[1][0], clipped_line[1][1]), 3)
                #             pygame.display.flip()
                #             detected.append(clipped_line)
                #             # print("CLIPPED", clipped_line)

                #         clipped_line_x = wall.rect.clipline(ray_x)
                #         if clipped_line_x:
                #             # detected.append(clipped_line)
                #             pygame.draw.line(SCREEN, (255, 30, 200), (clipped_line_x[0][0], clipped_line_x[0][1]),
                #                              (clipped_line_x[1][0], clipped_line_x[1][1]), 3)
                #             pygame.display.flip()
                #             detected_x.append(clipped_line_x)
                #             # print("CLIPPED", clipped_line)

                #         clipped_line_y = wall.rect.clipline(ray_y)
                #         if clipped_line_y:
                #             # detected.append(clipped_line)
                #             pygame.draw.line(SCREEN, (0, 30, 200), (clipped_line_y[0][0], clipped_line_y[0][1]),
                #                              (clipped_line_y[1][0], clipped_line_y[1][1]), 3)
                #             pygame.display.flip()
                #             detected_y.append(clipped_line_y)
                #             # print("CLIPPED", clipped_line)

                # if detected:
                #     next_x = 0
                #     next_y = 0

                #     if cur_pos[0] < next_pos[0]:

                #         min_x = 800
                #         if detected:
                #             for line in detected:
                #                 if line[0][0] < min_x:
                #                     min_x = line[0][0]
                #         if detected_x:
                #             for line in detected_x:
                #                 if line[0][0] < min_x:
                #                     min_x = line[0][0]
                #         if detected_y:
                #             for line in detected_y:
                #                 if line[0][0] < min_x:
                #                     min_x = line[0][0]

                #         next_x = min_x-ROBOT.get_width()

                #     elif cur_pos[0] >= next_pos[0]:

                #         max_x = 0
                #         if detected:
                #             for line in detected:
                #                 if line[0][0] > max_x:
                #                     max_x = line[0][0]
                #         if detected_x:
                #             for line in detected_x:
                #                 if line[0][0] < max_x:
                #                     max_x = line[0][0]
                #         if detected_y:
                #             for line in detected_y:
                #                 if line[0][0] < max_x:
                #                     max_x = line[0][0]

                #         next_x = max_x

                #     if cur_pos[1] < next_pos[1]:

                #         min_y = 800
                #         if detected:
                #             for line in detected:
                #                 if line[0][1] < min_y:
                #                     min_y = line[0][1]
                #         if detected_x:
                #             for line in detected_x:
                #                 if line[0][1] < min_y:
                #                     min_y = line[0][1]
                #         if detected_y:
                #             for line in detected_y:
                #                 if line[0][1] < min_y:
                #                     min_y = line[0][1]

                #         next_y = min_y - ROBOT.get_height()

                #     elif cur_pos[1] >= next_pos[1]:

                #         max_y = 0
                #         if detected:
                #             for line in detected:
                #                 if line[0][1] > max_y:
                #                     max_y = line[0][1]
                #         if detected_x:
                #             for line in detected_x:
                #                 if line[0][1] < max_y:
                #                     max_y = line[0][1]
                #         if detected_y:
                #             for line in detected_y:
                #                 if line[0][1] < max_y:
                #                     max_y = line[0][1]

                #         next_y = max_y

                #     next_pos = (next_x, next_y)

                # --------------------------------------

        right_collisions = []
        left_collisions = []
        top_collisions = []
        bottom_collisions = []
        for wall in wall_list:

            if cur_pos[0] == 40:
                print("here")

            # LEFT MOVEMENT
            if cur_pos[0] > next_pos[0]:
                clipped_line = wall.rect.clipline(
                    (cur_pos[0], cur_pos[1]), (next_pos[0], next_pos[1]))
                if clipped_line:

                    if clipped_line[0][0] < 400:
                        print("here")
                    if abs(clipped_line[0][0] - wall.rect.right) < 10:
                        # Right collision
                        right_collisions.append(clipped_line[0][0])
                    elif abs(next_pos[1] - wall.rect.bottom) < 10:
                        # Bottom collision
                        bottom_collisions.append(clipped_line[0][1])
                    elif abs(next_pos[1] - wall.rect.top) < 10:
                        # Top collision
                        top_collisions.append(
                            clipped_line[0][1] - self.img.get_height())
                    print(clipped_line)
            # RIGHT MOVEMENT
            elif cur_pos[0] < next_pos[0]:
                clipped_line = wall.rect.clipline(
                    (cur_pos[0], cur_pos[1]), (next_pos[0], next_pos[1]))
                if clipped_line:

                    if self.x > 696:
                        print("here")

                    if abs(clipped_line[0][0] - wall.rect.left) < 10:
                        # Left collision
                        left_collisions.append(clipped_line[0][0])
                    elif abs(next_pos[1] - wall.rect.bottom) < 10:
                        # Bottom collision
                        bottom_collisions.append(clipped_line[0][1])
                    elif abs(next_pos[1] - wall.rect.top) < 10:
                        # Top collision
                        top_collisions.append(
                            clipped_line[0][1] - self.img.get_height())
                    print(clipped_line)

            # UPWARD MOVEMENT
            if cur_pos[1] > next_pos[1]:
                clipped_line = wall.rect.clipline(
                    (cur_pos[0], cur_pos[1]), (next_pos[0], next_pos[1]))
                if clipped_line:
                    if abs(clipped_line[0][1] - wall.rect.bottom) < 10:
                        # Bottom collision
                        bottom_collisions.append(clipped_line[0][1])
                    elif abs(next_pos[1] == wall.rect.bottom) < 10:
                        # Left collision
                        left_collisions.append(
                            clipped_line[0][0] - self.img.get_width())
                    elif abs(next_pos[1] == wall.rect.top) < 10:
                        # Right collision
                        right_collisions.append(
                            clipped_line[0][0])
                    print(clipped_line)

            # BOTTOM MOVEMENT
            elif cur_pos[1] < next_pos[1]:
                clipped_line = wall.rect.clipline(
                    (cur_pos[0], cur_pos[1]), (next_pos[0], next_pos[1]))
                if clipped_line:
                    if abs(clipped_line[0][1] - wall.rect.top) < 10:
                        # Top collision
                        top_collisions.append(clipped_line[0][1])
                    elif abs(next_pos[1] - wall.rect.bottom) < 10:
                        # Left collision
                        left_collisions.append(
                            clipped_line[0][0] - self.img.get_width())
                    elif abs(next_pos[1] - wall.rect.top) < 10:
                        # Right collision
                        right_collisions.append(
                            clipped_line[0][0])
                    print(clipped_line)

        closest_x = 0
        closest_y = 0

        if right_collisions:
            closest_x = 0
            for crash in right_collisions:
                if crash > closest_x:
                    closest_x = crash
        elif left_collisions:
            closest_x = 10000
            for crash in left_collisions:
                if crash < closest_x:
                    closest_x = crash + 1

        if top_collisions:
            closest_y = 10000
            for crash in top_collisions:
                if crash < closest_y:
                    closest_y = crash+1

        elif bottom_collisions:
            closest_y = 0
            for crash in bottom_collisions:
                if crash > closest_y:
                    closest_y = crash-1

        temp_next_x = 0
        temp_next_y = 0

        if closest_x != 0:
            temp_next_x = closest_x
        if closest_y != 0:
            temp_next_y = closest_y

        if temp_next_x > 0:
            if temp_next_y > 0:
                next_pos = (temp_next_x, temp_next_y)
            else:
                next_pos = (temp_next_x, next_pos[1])
        else:
            if temp_next_y > 0:
                next_pos = (next_pos[0], temp_next_y)

            # --------------------------------------

            # if detected_x:
            #     if detected_y:
            #         next_pos = (detected_x[0][0][0], detected_y[0][0][1])
            #     else:
            #         next_pos = (detected_x[0][0][0], detected_x[0][0][1])
            # else:
            #     if detected_y:
            #         next_pos = (detected_y[0][0][0], detected_y[0][0][1])

            # min_distance = 1000000
            # if detected:
            #     for line in detected:
            #         print("NUMBER ", len(detected))
            #         line_distance = int(
            #             math.sqrt((line[1][1]-line[0][1])**2 + (line[1][0]-line[0][0])**2))
            #         if line_distance < min_distance:
            #             min_distance = line_distance
            #             clipped_line = line
            #     # pygame.draw.line(SCREEN, (255, 30, 9), (clipped_line[0][0], clipped_line[0][1]),
            #     #                  (clipped_line[1][0], clipped_line[1][1]), 3)
            #     # print("CLIPPED", clipped_line)

            #     for wall in wall_list:
            #         ray = (cur_pos[0], cur_pos[1]), (clipped_line[0]
            #                                          [0], clipped_line[0][1])
            #         second_clipped_line = wall.rect.clipline(ray)
            #         if second_clipped_line:
            #             next_pos = second_clipped_line[0]
            #         else:
            #             next_pos = clipped_line[0]

            # pygame.display.flip()
        for wall in wall_list:
            # for point in range(dif_range):
            #     if cur_pos[0] > next_pos[0]:
            #         if self.rect.collidepoint((cur_pos[0]-point), cur_pos[1]):
            #             print("Wall at", (cur_pos[0]-point), cur_pos[1])
            #             print("point = ", point)
            #             print("-")
            #             right_col[0] = True
            #             right_col[1] = wall.rect.right
            #             return uper_col, bottom_col, right_col, left_col
            # else:
            #     if self.rect.collidepoint((cur_pos[0]+point), cur_pos[1]):
            #         print("Wall at", (cur_pos[0]+point), cur_pos[1])
            #         print("point = ", point)
            #         print("-")
            #         left_col[0] = True
            #         left_col[1] = wall.rect.left - ROBOT.get_width()
            #         return uper_col, bottom_col, right_col, left_col
            # elif abs(cur_pos[1] - next_pos[1]) > 30:
            #     pygame.draw.line(SCREEN, (255, 255, 0), (cur_pos[0], cur_pos[1]),
            #                      (next_pos[0], next_pos[1]), 3)
            #     pygame.display.flip()

            #     dif_range = int(abs(cur_pos[0] - next_pos[0]))

            #     for point in range(dif_range):
            #         if cur_pos[1] > next_pos[1]:
            #             if self.rect.collidepoint(next_pos[0], (cur_pos[1]-point)):
            #                 print("Wall at", next_pos[0], (cur_pos[1]-point))
            #                 print("point = ", point)
            #                 print("-")
            #                 uper_col[0] = True
            #                 uper_col[1] = (cur_pos[1]-point)
            #                 return uper_col, bottom_col, right_col, left_col
            #         else:
            #             if self.rect.collidepoint(next_pos[0], (cur_pos[1]+point)):
            #                 print("Wall at", (next_pos[0], (cur_pos[1]+point)))
            #                 print("point = ", point)
            #                 print("-")
            #                 bottom_col[0] = True
            #                 bottom_col[1] = (cur_pos[1]+point)
            #                 return uper_col, bottom_col, right_col, left_col

            next_rect = pygame.Rect(
                next_pos[0], next_pos[1], self.img.get_width(), self.img.get_height())

            if next_rect.colliderect(wall.rect):

                if abs(wall.rect.top - self.rect.bottom) <= 10:
                    # print("upper col")
                    uper_col[0] = True
                    uper_col[1] = wall.rect.top - self.img.get_height()
                elif abs(wall.rect.bottom - self.rect.top) <= 10:
                    # print("bottom col")
                    bottom_col[0] = True
                    bottom_col[1] = wall.rect.bottom

                if abs(wall.rect.right - self.rect.left) <= 10:
                    # print("right col")
                    right_col[0] = True
                    right_col[1] = wall.rect.right
                elif abs(wall.rect.left - self.rect.right) <= 10:
                    # print("left col")
                    left_col[0] = True
                    left_col[1] = wall.rect.left - self.img.get_width()

        return uper_col, bottom_col, right_col, left_col

    def collide(self, cur_pos, next_pos, width, height):
        self.boundaryX = width - 64
        self.boundaryY = height - 64
        # hit the wall
        if self.x <= 41:
            self.x = 41
            if self.hasCollided != True:
                self.wallCollisions += 1
            self.hasCollided = True

        elif self.x >= self.boundaryX - 42:
            self.x = self.boundaryX - 42
            if self.hasCollided != True:
                self.wallCollisions += 1
            self.hasCollided = True

        if self.y <= 41:
            self.y = 41
            if self.hasCollided != True:
                self.wallCollisions += 1
            self.hasCollided = True

        elif self.y >= self.boundaryY - 42:
            self.y = self.boundaryY - 42
            if self.hasCollided != True:
                self.wallCollisions += 1
            self.hasCollided = True

    def collide2(self, cur_pos, next_pos, wall_list):

        u_col, b_col, r_col, l_col = self.is_colliding(
            cur_pos, next_pos, wall_list)

        if u_col[0] or b_col[0] or r_col[0] or l_col[0]:
            if self.hasCollided != True:
                self.wallCollisions += 1
            self.hasCollided = True
        else:
            self.hasCollided = False

        if l_col[0]:
            self.x = l_col[1]

        elif r_col[0]:
            self.x = r_col[1]

        else:
            self.x = next_pos[0]

        if u_col[0]:
            self.y = u_col[1]

        elif b_col[0]:
            self.y = b_col[1]

        else:
            self.y = next_pos[1]


class PlayRobot(RobotMove):
    # START_POS = (random.uniform(40, 735), random.uniform(
    #     40, 535))  # start at random potition
    START_POS = (550, 300)
    trail_set = []


# Raycasting


def cast_rays(screen, walls, player_robot, ROBOT, STEP_ANGLE, SENSORS_FONT):

    all_sensors = []

    sensor_x = player_robot.x+(ROBOT.get_width()/2)
    sensor_y = player_robot.y+(ROBOT.get_height()/2)

    temp_angle = 0
    for i in range(12):
        all_sensors.append((sensor_x, sensor_y, temp_angle, temp_angle, i))
        temp_angle += STEP_ANGLE

    for sensor in all_sensors:

        clipped_line = None

        sensor_placement_offset = 8
        sensor_placement_radius_depth = 64
        sensor_placement_x = sensor[0] - math.sin(
            sensor[2]) * sensor_placement_radius_depth - sensor_placement_offset
        sensor_placement_y = sensor[1] + math.cos(
            sensor[3]) * sensor_placement_radius_depth - sensor_placement_offset
        collision_offset = 32

        for depth in range(200):
            target_x = sensor[0] - math.sin(sensor[2]) * depth
            target_y = sensor[1] + math.cos(sensor[3]) * depth

            ray = ((sensor_x, sensor_y), (target_x, target_y))

            detected = []

            for i in range(len(walls)):
                clipped_line = walls[i].clipline(ray)
                if clipped_line:
                    detected.append(clipped_line)

        sensor_distance = 200
        if detected:
            for line in detected:
                temp_sensor_distance = int(
                    math.sqrt((line[0][1]-sensor_y)**2 + (line[0][0]-sensor_x)**2))-collision_offset
                if temp_sensor_distance < sensor_distance:
                    sensor_distance = temp_sensor_distance
                    clipped_line = line

            pygame.draw.line(screen, (255, 130, 100), (sensor_x, sensor_y),
                             (clipped_line[0][0], clipped_line[0][1]), 3)

        sensor_text = SENSORS_FONT.render(
            f"{sensor_distance}", 1, (255, 255, 255))
        screen.blit(
            sensor_text, (sensor_placement_x, sensor_placement_y))

    # ------------


def dustEncountered(self, dustImg):

    for dust in dustImg:
        if self.rect.colliderect(dust.rect):
            self.dustCleared += 1
            print("Dust", self.dustCleared)
            dustImg.remove(dust)


def find_line(x_start, y_start, x_end, y_end):
    points = [(x_start, y_start), (x_end, y_end)]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]
    print("Line Solution is y = {m}x + {c}".format(m=m, c=c))

# setting the enviroment


class Envir:
    def __init__(self, dimension):
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        # map_dims
        self.height = dimension[0]
        self.width = dimension[1]
        # window setting
        self.map = pygame.display.set_mode((self.width, self.height))
        # trail
        self.trail_set = []
        self.dust_remaining = 0
    # line route

    def trail(self, pos):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(self.map, self.white, (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__() > 10000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)
    # y and x axis

    def robot_frame(self, pos, rotation, robot):
        n = 80
        # centerx, centery = pos
        centerx = pos[0]+(robot.get_width()/2)
        centery = pos[1]+(robot.get_height()/2)
        x_axis = (centerx + n*np.cos(rotation), centery + n*np.sin(rotation))
        y_axis = (centerx + n*np.cos(rotation+np.pi/2),
                  centery + n*np.sin(rotation+np.pi/2))
        pygame.draw.line(self.map, self.black, (centerx, centery), x_axis, 3)
        pygame.draw.line(self.map, self.black, (centerx, centery), y_axis, 3)

    def dustCheck(self, dustImg):
        self.dust_remaining = len(dustImg)

    def draw(self, screen, images, player_robot, MAIN_FONT, HEIGHT):

        # display images on screen
        for img, pos, name in images:
            screen.blit(img, pos)

        # display left, right velocity and theta on screen
        vel_text = MAIN_FONT.render(
            f"Vl = {round(player_robot.vl,2)} Vr = {round(player_robot.vr,2)} theta = {int(np.degrees(player_robot.theta))}", 1, self.white)
        screen.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 40))

        # display robot on screen
        player_robot.draw(screen)
        # pygame.display.update()

    def setWalls(HEIGHT, WIDTH):
        wall_pixel_offset = 42
        rectWallL = pygame.Rect(0, 0, wall_pixel_offset, HEIGHT)
        rectWallR = pygame.Rect(WIDTH-wall_pixel_offset, 0,
                                wall_pixel_offset, HEIGHT)
        rectWallT = pygame.Rect(0,  0, WIDTH, wall_pixel_offset)
        rectWallB = pygame.Rect(0, HEIGHT-wall_pixel_offset,
                                WIDTH, wall_pixel_offset)
        return [rectWallL, rectWallR, rectWallT, rectWallB]


class Wall():
    def __init__(self, x, y, width, height, transparency):
        self.rect = pygame.Rect(x, y, width, height)
        self.istransparent = transparency

    def draw(self, screen):
        if not self.istransparent:
            pygame.draw.rect(screen, (0, 51, 0), self.rect)


class Dust:
    def __init__(self, x, y, img, id):
        self.x = x
        self.y = y
        self.img = img
        self.rect = pygame.Rect(x, y, img.get_width(), img.get_height())
        self.id = id

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Robot(object):

    def __init__(self, weights):
        self.Main(weights)

    def Main(self, NN):
        pygame.init()

        inputs = np.random.rand(1, 10)

        # images
        BACKGROUND = pygame.image.load("images/background.png")
        ROBOT = pygame.image.load("images/vacuum.png")
        ICON = pygame.image.load('images/icon.png')
        DUST = pygame.image.load('images/dust.png')

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
        STEP_ANGLE = (math.pi * 2) / 12
        # -------

        images = [(BACKGROUND, (0, 0), "bg")]
        # the robot
        # player_robot = PlayRobot()
        # walls

        wall_pixel_offset = 42
        wall_list = [Wall(110, 200, 291, 20, False), Wall(400, 39, 20, 300, False), Wall(0, 0, wall_pixel_offset-1, HEIGHT, True),
                     Wall(WIDTH-wall_pixel_offset, 0, wall_pixel_offset, HEIGHT,
                          True), Wall(0,  0, WIDTH, wall_pixel_offset-1, True),
                     Wall(0, HEIGHT-wall_pixel_offset, WIDTH, wall_pixel_offset, True)]

        dustImg = [(Dust(340, 340, DUST, 1)), Dust(440, 440, DUST, 2), (Dust(500, 500, DUST, 3)), (Dust(
            80, 150, DUST, 4)), (Dust(240, 100, DUST, 5)), (Dust(500, 127, DUST, 6)), (Dust(122, 250, DUST, 7))]

        # enviroment prints
        environment = Envir([600, 800])
        walls = Envir.setWalls(HEIGHT, WIDTH)

        for wall in wall_list:
            walls.append(wall.rect)

        player_robot = PlayRobot(ROBOT)

        # dt
        dt = 50
        clock = pygame.time.Clock()
        FPS = 60

        # simulation loop
        for _ in range(500):

            [vl, vr] = NN.forward_propagate(inputs)[1]
            activate2 = player_robot.simulation_move(
                vl, vr, dt, wall_list, SCREEN)
            #motor = NN.forward_propagate(inputs)
            print('motor: ', [vl, vr])
            # activate quit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # timer
            clock.tick(FPS)

            # activate buttons
            keys = pygame.key.get_pressed()
            key = [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_o], keys[pygame.K_l],
                   keys[pygame.K_t], keys[pygame.K_g], keys[pygame.K_x]]

            # run the robot
            activate = player_robot.move(key, dt, wall_list, SCREEN)
            # player_robot.collide(WIDTH, HEIGHT)

            # visualize objects

            # wall_collision(player_robot, SCREEN, WallRect)
            dustEncountered(player_robot, dustImg)
            environment.draw(SCREEN, images, player_robot, MAIN_FONT, HEIGHT)
            for wall in wall_list:
                wall.draw(SCREEN)
            for dust in dustImg:
                dust.draw(SCREEN)
            environment.dustCheck(dustImg)
            # print("Dust remaining ", environment.dust_remaining)
            # print("Wall Collisions", player_robot.wallCollisions)
            environment.robot_frame(
                (player_robot.x, player_robot.y), player_robot.theta, player_robot.img)
            environment.trail((player_robot.x + (ROBOT.get_width()/2),
                               player_robot.y + (ROBOT.get_height()/2)))
            player_robot.upd_rect()
            player_robot.draw(environment.map)
            cast_rays(SCREEN, walls, player_robot,
                      ROBOT, STEP_ANGLE, SENSORS_FONT)

            # ---

            pygame.display.update()

        # exit the game
        pygame.quit()
