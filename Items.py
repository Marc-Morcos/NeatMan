import pygame
from Constants import *
import random

class Pellet:
    def __init__(self, x, y,sparseFlipped = False):
        self.array_coord = [x, y]
        self.x = x * block_size + half_block_size
        self.y = y * block_size + half_block_size

        self.colour = (255, 255, 255)

        self.here = True
        if(sparseFlipped and neatMode): self.here = random.choice([False,False,False,False,True])

    def draw(self, display):
        if self.here:
            half = pellet_size/2
            pygame.draw.ellipse(display, self.colour, (self.x - half, self.y - half + offset,
                                                                pellet_size, pellet_size))

    def collide(self, player):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < pellet_size and dist_y < pellet_size and self.here:
            self.here = False
            return True
        
        return False


class PowerPellet:
    def __init__(self, x, y,generation):
        self.array_coord = [x, y]
        self.x = x * block_size + half_block_size
        self.y = y * block_size + half_block_size

        if ((not ((generation%disablePowerPelletsEvery==0) and (disablePowerPellets))) or not neatMode):
            self.here = True
        else:
            self.here = False

    def draw(self, display):
        if self.here:
            half = power_pellet_size/2
            pygame.draw.ellipse(display, (255, 255, 255), (self.x - half, self.y - half + offset,
                                                                power_pellet_size, power_pellet_size))

    def collide(self, player):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < power_pellet_size and dist_y < power_pellet_size and self.here:
            self.here = False
            return True

        return False

class Fruit:
    def __init__(self, x, y, score, image, here):
        self.array_coord = [x, y]
        self.x = x * block_size + half_block_size
        self.y = y * block_size + half_block_size

        self.score = score
        self.image = image

        self.time = 0
        self.here = here

    def update(self):
        if self.here:
            self.time -= 1

            if self.time == 0:
                self.here = False

    def draw(self, display):
        if self.here:
            display.blit(self.image, (self.x - half_block_size, self.y - half_block_size + offset))

    def collide(self, player):
        if self.here:
            dist_x = abs(self.x - player.x)
            dist_y = abs(self.y - player.y)

            if dist_x < half_block_size and dist_y < half_block_size:
                self.here = False
                return self.score

        return 0