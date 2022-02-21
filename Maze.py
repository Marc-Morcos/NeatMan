import pygame
import Ghost
from mazegen.mapGenClean import createMap
from Constants import *

class Maze:
    def __init__(self, maze_width, maze_height):
        self.power_pellet_locs = [(1,2),(17,15),(1,15),(17,2)] #default, these get overwritten by the mapgen

        # draw maze
        self.maze_array = [[0] * maze_width for i in range(maze_height)]  # [y][x]

        if maze_width == 28 and maze_height == 31:
            self.wall_locs, self.pellet_locs, self.power_pellet_locs, self.ghost_door_locs = createMap(self.maze_array)

    def draw(self, display):
        # draw maze
        for wall in self.wall_locs:
            pygame.draw.rect(display, (0, 0, 210), (wall[0] * block_size, wall[1] * block_size + offset, block_size, block_size))

        for ghost_door in self.ghost_door_locs:
            pygame.draw.rect(display, (200, 0, 0), (ghost_door[0] * block_size, ghost_door[1] * block_size + offset, block_size, block_size))

    def center(self, entity, var, coord):
        setattr(entity, var, int(coord / block_size) * block_size + block_size / 2)

    def can_move(self, entity, dir):
        allowed = [0, 3, 4]
        if isinstance(entity, Ghost.Ghost):
            if (entity.mode == "normal" and house_x <= entity.array_coord[0] <= house_x+2 and house_y-1 <= entity.array_coord[1] <= house_y+2) \
                    or entity.mode == "dead":
                allowed = [0, 2, 3]
            elif dir == UP:
                allowed = [0, 3]

        if dir == UP or dir == DOWN:
            x_plus = int((entity.x + block_size / 2 - entity.step) / block_size)
            x_minus = int((entity.x - block_size / 2 + entity.step) / block_size)
            tmp_y = int((entity.y - block_size / 2 - entity.step) / block_size)
            if dir == DOWN:
                tmp_y = int((entity.y + block_size / 2 + entity.step) / block_size)
            if self.maze_array[tmp_y][x_plus] in allowed and self.maze_array[tmp_y][x_minus] in allowed:
                return True
        elif dir == LEFT or dir == RIGHT:
            y_plus = int((entity.y + block_size / 2 - entity.step) / block_size)
            y_minus = int((entity.y - block_size / 2 + entity.step) / block_size)
            tmp_x = int((entity.x - block_size / 2 - entity.step) / block_size)
            if dir == RIGHT:
                tmp_x = int((entity.x + block_size / 2 + entity.step) / block_size)
            if self.maze_array[y_plus][tmp_x] in allowed and self.maze_array[y_minus][tmp_x] in allowed:
                return True
        else:
            return False
