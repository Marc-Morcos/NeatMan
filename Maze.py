import pygame
import Ghost
from mazegen.mapGenClean import createMap
from Ghost import theGhostHousePosx,theGhostHousePosy

class Maze:
    def __init__(self, display, main):
        self.main = main
        self.display = display
        self.block_size = main.block_size
        self.offset = main.offset

        # draw maze
        self.maze_array = [[0] * main.maze_width for i in range(main.maze_height)]  # [y][x]
        
        if main.maze_width == 28 and main.maze_height == 31:
            powerUpLocations = createMap(self.maze_array)
            #todo use poweruplocations

    def draw(self):
        # draw maze
        for i in range(self.main.maze_width):
            for j in range(self.main.maze_height):
                if self.maze_array[j][i] == 1:
                    pygame.draw.rect(self.display, (0, 0, 210), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))
                elif self.maze_array[j][i] == 2:
                    pygame.draw.rect(self.display, (200, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))
                else:
                    pygame.draw.rect(self.display, (0, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                               self.block_size, self.block_size))

    def center(self, entity, var, coord):
        setattr(entity, var, int(coord / self.block_size) * self.block_size + self.block_size / 2)

    def can_move(self, entity, dir):
        allowed = [0, 3, 4]
        if isinstance(entity, Ghost.Ghost):
            if (entity.mode == "normal" and theGhostHousePosx <= entity.array_coord[0] <= theGhostHousePosx+2 and theGhostHousePosy-1 <= entity.array_coord[1] <= theGhostHousePosy+2) \
                    or entity.mode == "dead":
                allowed = [0, 2, 3]
            elif dir == entity.DIR["UP"]:
                allowed = [0, 3]

        if dir == entity.DIR["UP"] or dir == entity.DIR["DOWN"]:
            x_plus = int((entity.x + self.block_size / 2 - entity.step) / self.block_size)
            x_minus = int((entity.x - self.block_size / 2 + entity.step) / self.block_size)
            tmp_y = int((entity.y - self.block_size / 2 - entity.step) / self.block_size)
            if dir == entity.DIR["DOWN"]:
                tmp_y = int((entity.y + self.block_size / 2 + entity.step) / self.block_size)
            if self.maze_array[tmp_y][x_plus] in allowed and self.maze_array[tmp_y][x_minus] in allowed:
                return True
        elif dir == entity.DIR["LEFT"] or dir == entity.DIR["RIGHT"]:
            y_plus = int((entity.y + self.block_size / 2 - entity.step) / self.block_size)
            y_minus = int((entity.y - self.block_size / 2 + entity.step) / self.block_size)
            tmp_x = int((entity.x - self.block_size / 2 - entity.step) / self.block_size)
            if dir == entity.DIR["RIGHT"]:
                tmp_x = int((entity.x + entity.block_size / 2 + entity.step) / self.block_size)
            if self.maze_array[y_plus][tmp_x] in allowed and self.maze_array[y_minus][tmp_x] in allowed:
                return True
        else:
            return False
