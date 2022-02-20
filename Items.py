import pygame
from Constants import *

class Pellet:
    def __init__(self, x, y):
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2
        self.offset = block_size*2

        self.here = True

    def draw(self, display):
        if self.here:
            half = pellet_size/2
            pygame.draw.ellipse(display, (255, 255, 255), (self.x - half, self.y - half + self.offset,
                                                                pellet_size, pellet_size))

    def collide(self, player):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < pellet_size and dist_y < pellet_size and self.here:
            self.here = False
            return True
        
        return False


class PowerPellet:
    def __init__(self, x, y):
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2

        self.here = True

    def draw(self, display):
        if self.here:
            offset = block_size*2
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
