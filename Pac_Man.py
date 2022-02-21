import pygame
import Ghost
import math
from Constants import *

class Pac_Man:
    def __init__(self, x, y, movementFunction):
        self.movementFunction = movementFunction
        # Constants
        self.size = 26
        self.step_len = block_size / 15
        self.step = self.step_len

        # Movement directions
        self.DIR = {"RIGHT": 0, "DOWN": 1, "LEFT": 2, "UP": 3}
        self.COORD_DIR = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
        self.look_dir = 3
        self.move_dir = 3

        # Location in pixels
        self.array_coord = [x, y]
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2

        # Setup vars
        self.powered_up = False
        self.timer = 0
        self.power_time = 0
        self.ghosts_eaten = 0

    def power_up(self, time):
        self.powered_up = True
        self.power_time = time
        self.timer = 0

    def update_power_up(self):
        if self.powered_up:
            # end power up at end of timer
            if self.timer >= self.power_time:
                self.powered_up = False
                self.ghosts_eaten = 0
                return False
            else:
                self.timer += 1

            return True

        return False

    def move(self, maze, display_width):
        self.look_dir = self.movementFunction()
        step = self.step_len
        self.array_coord = [int((self.x + block_size / 2) / block_size),
                            int((self.y + block_size / 2) / block_size)]

        # Can only change direction within the bounds of the maze
        if block_size < self.x < display_width - block_size:
            # Change movement direction to match look direction if possible
            if self.look_dir != self.move_dir:
                if maze.can_move(self, self.look_dir):
                    self.move_dir = self.look_dir

            # Do movement
            if maze.can_move(self, self.move_dir):
                self.x += step * self.COORD_DIR[self.move_dir][0]
                self.y += step * self.COORD_DIR[self.move_dir][1]

        # If outside maze, keep moving forwards until wrapped to the other side of the screen
        else:
            maze.center(self, "y", self.y)
            if self.move_dir == self.DIR["LEFT"]:
                self.x -= step
            if self.move_dir == self.DIR["RIGHT"]:
                self.x += step
            # Screen wrap
            if self.x < -self.size:
                self.x = display_width
            if self.x > self.size + display_width:
                self.x = -self.size

    def draw_wedge_pacman(self, display, wedge_angle):
        radius = self.size / 2
        n_points = 60
        point_separation = math.radians((360 - wedge_angle) / n_points)
        current_angle = math.radians(90 * self.move_dir + wedge_angle / 2)
        pointlist = [(self.x, self.y + offset) for i in range(n_points)]

        for i in range(1, n_points):
            pointlist[i] = (self.x + math.cos(current_angle) * radius,
                            self.y + math.sin(current_angle) * radius + offset)
            current_angle += point_separation

        pygame.draw.polygon(display, (255, 255, 0), pointlist)

    def draw_while_running(self, display, display_width, maze, tick_counter):
        if (not block_size/2 < self.x < display_width - block_size/2 - self.size) \
                or maze.can_move(self, self.move_dir):
            if tick_counter % 18 < 9:
                self.draw_wedge_pacman(display, (tick_counter % 9) * 15)
            else:
                self.draw_wedge_pacman(display, 120 - (tick_counter % 9) * 15)
        else:
            self.draw_wedge_pacman(display, 75)
