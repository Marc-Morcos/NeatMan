import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from operator import *
import math
from Pac_Man import Pac_Man
import numpy as np

#returns grid index for 1D array
def gridToArray(x,y):
    return y*MapSizeX+x

#Process the inputs for the nead model 
#just passing in everything (SET inputs IN neatConfig to 912)
def NaiveNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit):
    #converting the inputs to a 1D array to pass into NEAT
    inputs = np.array(maze.maze_array)
    inputs = inputs.flatten()
    
    #tell ai about fruit
    inputs = np.append(inputs,[fruit.here, fruit.x, fruit.y])

    #tell ai about power pellets
    for power_pellet in power_pellets:
        inputs = np.append(inputs,[power_pellet.here, power_pellet.x, power_pellet.y])
    
    #tell ai about ghosts (boo)
    for ghost in ghosts.values():
        inputs = np.append(inputs,[ghost.x, ghost.y, ghost.blue, ghost.move_dir, (ghost.mode == "normal"), (pacman.power_time - ghost.blue_timer)])
    
    #tell ai about pacman
    inputs = np.append(inputs,[pacman.x, pacman.y, pacman.move_dir, pacman.powered_up, (pacman.power_time - pacman.timer)])

    return inputs

#Process the inputs for the nead model 
#this gives the input a grid, always shown at least a quarter of the map if not the full thing, 
# with pacman in the center (SET inputs IN neatConfig to 887)
def cameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit):
    inputs = np.zeros(887)

    #everything is with respect to pacman
    xOffset = int(pacman.array_coord[0] - MapSizeX/2)
    yOffset = int(pacman.array_coord[1] - MapSizeY/2)

    #the order in which we add these is important since multiple things can be in the same spot

    #add visible pellets to the grid
    for pellet in pellets:
        if pellet.here:
            relativeX = pellet.array_coord[0] - xOffset
            relativeY = pellet.array_coord[1] - yOffset
            if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
                inputs[gridToArray(relativeX, relativeY)] = 1

    #add visible power pellets to the grid
    for powerPellet in power_pellets:
        if powerPellet.here:
            relativeX = powerPellet.array_coord[0] - xOffset
            relativeY = powerPellet.array_coord[1] - yOffset
            if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
                inputs[gridToArray(relativeX, relativeY)] = 3

    #add visible fruit to the grid
    if fruit.here:
        relativeX = fruit.array_coord[0] - xOffset
        relativeY = fruit.array_coord[1] - yOffset
        if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
            inputs[gridToArray(relativeX, relativeY)] = 2

    #add visible walls to the grid
    for wall in maze.wall_locs:
        relativeX = wall[0] - xOffset
        relativeY = wall[1] - yOffset
        if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
            inputs[gridToArray(relativeX, relativeY)] = -1
    for wall in maze.ghost_door_locs: #ghost doors are basically walls
        relativeX = wall[0] - xOffset
        relativeY = wall[1] - yOffset
        if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
            inputs[gridToArray(relativeX, relativeY)] = -1

    #add visible ghosts to the grid
    for ghost in ghosts.values():
        relativeX = ghost.array_coord[0] - xOffset
        relativeY = ghost.array_coord[1] - yOffset
        if(relativeX>=0 and relativeY>=0 and relativeX<MapSizeX and relativeY<MapSizeY):
            inputs[gridToArray(relativeX, relativeY)] = -3

    #add extra info
    index = 868
    for ghost in ghosts.values():
        inputs[index] = ghost.blue
        index+=1
        inputs[index] = ghost.move_dir
        index+=1
        inputs[index] = (ghost.mode == "normal")
        index+=1
        inputs[index] = (pacman.power_time - ghost.blue_timer)
        index+=1

    inputs[index] = pacman.move_dir
    index+=1
    inputs[index] = pacman.powered_up
    index+=1
    inputs[index] = (pacman.power_time - pacman.timer)

    return inputs        


#nead model controller
def modelNeat(pacman, maze, ghosts, pellets, power_pellets, fruit):
    
    #Get the inputs
    inputs = cameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit)

    #pass inputs into the neural network
    outputs = pacman.net.activate(inputs)
    
    #interpret net output 
    max = outputs[0]
    max_id = 0
    for output_id in range(len(outputs)):
        if outputs[output_id] > max:
            max = outputs[output_id]
            max_id = output_id

    return max_id

#random moves -> no smart
def dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pac_man.move_dir

#human controlled pac_man
def humanPlayer(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    return pac_man.humanInput

#avoid ghosts
def avoid_ghost_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    avoid_distance = 100
    possible_dirs = set([RIGHT, LEFT, UP, DOWN])

    for ghost in ghosts.values():
        if ghost.mode == "normal":
            # Remove directions that are near an active ghost
            if 0 < ghost.x - pac_man.x < avoid_distance:
               possible_dirs -= set([RIGHT])

            if 0 < pac_man.x - ghost.x < avoid_distance:
                possible_dirs -= set([LEFT])

            if 0 < ghost.y - pac_man.y < avoid_distance:
               possible_dirs -= set([DOWN])

            if 0 < pac_man.y - ghost.y < avoid_distance:
                possible_dirs -= set([UP])

    # Select a random direction out of the possible directions
    if possible_dirs:
        return random.sample(possible_dirs, 1)[0]
    return pac_man.move_dir

#avoid ghosts and walls
def avoid_ghost_and_walls_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    avoid_distance = 100
    possible_dirs = set([RIGHT, LEFT, UP, DOWN])

    for ghost in ghosts.values():
        dist = abs(ghost.x - pac_man.x) + abs(ghost.y - pac_man.y)

        if ghost.mode == "normal" and dist < avoid_distance:
            # Remove directions that are near an active ghost
            if 0 < ghost.x - pac_man.x:
               possible_dirs -= set([RIGHT])

            if 0 < pac_man.x - ghost.x:
                possible_dirs -= set([LEFT])

            if 0 < ghost.y - pac_man.y:
               possible_dirs -= set([DOWN])

            if 0 < pac_man.y - ghost.y:
                possible_dirs -= set([UP])

    # Remove directions that are a wall
    if not maze.can_move(pac_man, RIGHT):
        possible_dirs -= set([RIGHT])

    if not maze.can_move(pac_man, LEFT):
        possible_dirs -= set([LEFT])

    if not maze.can_move(pac_man, UP):
        possible_dirs -= set([UP])

    if not maze.can_move(pac_man, DOWN):
        possible_dirs -= set([DOWN])

    # Select a random direction out of the possible directions
    if possible_dirs:
        return random.sample(possible_dirs, 1)[0]
    return pac_man.move_dir

#avoid ghosts and walls with target pellet
def avoid_gw_w_tp_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    avoid_distance = 60
    possible_dirs = set([RIGHT, LEFT, UP, DOWN])

    for ghost in ghosts.values():
        dist = abs(ghost.x - pac_man.x) + abs(ghost.y - pac_man.y)

        if ghost.mode == "normal" and dist < avoid_distance:
            # Remove directions that are near an active ghost
            if 0 < ghost.x - pac_man.x:
               possible_dirs -= set([RIGHT])

            if 0 < pac_man.x - ghost.x:
                possible_dirs -= set([LEFT])

            if 0 < ghost.y - pac_man.y:
               possible_dirs -= set([DOWN])

            if 0 < pac_man.y - ghost.y:
                possible_dirs -= set([UP])


    # Remove directions that are a wall


    '''
    if not maze.can_move(pac_man, RIGHT):
        possible_dirs -= set([RIGHT])

    if not maze.can_move(pac_man, LEFT):
        possible_dirs -= set([LEFT])

    if not maze.can_move(pac_man, UP):
        possible_dirs -= set([UP])

    if not maze.can_move(pac_man, DOWN):
        possible_dirs -= set([DOWN])
    '''

    if not pac_man.target or not pac_man.target.here:
        pac_man.target = pellets[0]
        min_dist = 100000000

        for pellet in pellets:
            if pellet.here:
                #print("Target: {}, {}   Pellet: {}, {}".format(target.x, target.y, pellet.x, pellet.y))
                dist = abs(pellet.x - pac_man.x) + abs(pellet.y - pac_man.y)

                if dist < min_dist:
                    pac_man.target = pellet
                    min_dist = dist

        pac_man.target.colour = (255, 0, 0)

        #print("Pac-Man: {}, {}  Target: {}, {}  Dist: {}".format(pac_man.x, pac_man.y, pac_man.target.x, pac_man.target.y, dist))


    if not maze.can_move(pac_man, pac_man.move_dir):
        if pac_man.try_move_dir == pac_man.move_dir:
            pac_man.try_move_dir = (pac_man.move_dir + random.choice((-1, 1))) % 4
        if pac_man.try_move_dir in possible_dirs:
            return pac_man.try_move_dir
        elif possible_dirs:
            return random.sample(possible_dirs, 1)
        return pac_man.move_dir
    else:
        pac_man.try_move_dir = pac_man.move_dir

    # if in a dead end, flip direction
    if not (maze.can_move(pac_man, pac_man.try_move_dir)) \
            and not (maze.can_move(pac_man, left_turn(pac_man.try_move_dir))) \
            and not (maze.can_move(pac_man, right_turn(pac_man.try_move_dir))):
        pac_man.try_move_dir = (pac_man.try_move_dir+2) % 4

    return pac_man.try_move_dir


#broken do not use
def target_pellet_withGhostAi(pac_man, maze, ghosts, pellets, power_pellets, fruit):


    #code adapted from the ghost ai
    def find_distance(a_pos, b_pos):
        a = pow(abs(a_pos[0] - b_pos[0]), 2)
        b = pow(abs(a_pos[1] - b_pos[1]), 2)
        return math.sqrt(a + b)

    def find_closest(facing, target_pos):
        return_dir = facing
        next_pos = list(map(add, pac_man.array_coord, pac_man.COORD_DIR[facing]))
        dir_min = find_distance(next_pos, target_pos)
        # check left turn
        if maze.can_move(pac_man, left_turn(facing)):
            next_pos = list(map(add, pac_man.array_coord, pac_man.COORD_DIR[left_turn(facing)]))
            next_dir = find_distance(next_pos, target_pos)
            if next_dir < dir_min:
                dir_min = next_dir
                return_dir = left_turn(facing)
        # check right turn
        if maze.can_move(pac_man, right_turn(facing)):
            next_pos = list(map(add, pac_man.array_coord, pac_man.COORD_DIR[right_turn(facing)]))
            next_dir = find_distance(next_pos, target_pos)
            if next_dir < dir_min:
                return_dir = right_turn(facing)
        return return_dir

    def left_turn(facing):
        return abs((facing - 1) % 4)

    def right_turn(facing):
        return abs((facing + 1) % 4)



    #finds safe directions
    possible_dirs = set([RIGHT, LEFT, UP, DOWN])
    # Only try changing direction if within bounds of maze array
    if block_size < pac_man.x < pac_man.display_width - block_size:
        pac_man_row = int(pac_man.y / block_size)
        pac_man_col = int(pac_man.x / block_size)

        # Check whether the ghosts are visible from this player's perspective
        # If they are on the same row or column, check all tiles in between
        # If there are no walls, the ghost can see the player
        see_ghost= False
        for ghost in ghosts.values():
            wall = True
            ghost_dir = DOWN
            ghost_row = int(ghost.y / block_size)
            ghost_col = int(ghost.x / block_size)
            if pac_man_row == ghost_row or ghost_col == pac_man_col:
                wall = False  # flag for whether there is an obstruction between ghost and player
                if pac_man_col == ghost_col and pac_man_row == ghost_row:
                    wall = True
                elif pac_man_row == ghost_row:
                    if pac_man_col > ghost_col:
                        ghost_dir = LEFT
                        for i in range(0, pac_man_col - ghost_col):
                            if maze.maze_array[pac_man_row][i + ghost_col] == 1:
                                wall = True
                    elif ghost_col == pac_man_col:
                        wall = True
                    else:
                        ghost_dir = RIGHT
                        for i in range(0, ghost_col - pac_man_col):
                            if maze.maze_array[pac_man_row][i + pac_man_col] == 1:
                                wall = True
                elif pac_man_col == ghost_col:
                    if pac_man_row > ghost_row:
                        ghost_dir = UP
                        for i in range(0, pac_man_row - ghost_row):
                            if maze.maze_array[i + ghost_row][pac_man_col] == 1:
                                wall = True
                    elif ghost_row == pac_man_row:
                        wall = True
                    else:
                        ghost_dir = DOWN
                        for i in range(0, ghost_row - pac_man_row):
                            if maze.maze_array[i + pac_man_row][pac_man_col] == 1:
                                wall = True
            if not wall:
                see_ghost = True
                possible_dirs -= set([ghost_dir])

        # Remove directions that are a wall
        if not maze.can_move(pac_man, RIGHT):
            possible_dirs -= set([RIGHT])

        if not maze.can_move(pac_man, LEFT):
            possible_dirs -= set([LEFT])

        if not maze.can_move(pac_man, UP):
            possible_dirs -= set([UP])

        if not maze.can_move(pac_man, DOWN):
            possible_dirs -= set([DOWN])

        #generate target
        if(possible_dirs):
            next_dir = random.sample(possible_dirs, 1)[0]
        else:
            next_dir = DOWN
        target_coord = [0,0]

        # move towards target, only attempt a turn at an intersection
        if pac_man.step < pac_man.x % block_size < block_size - pac_man.step \
                and pac_man.step < pac_man.y % block_size < block_size - pac_man.step:
            if maze.can_move(pac_man, left_turn(next_dir)) \
                    or maze.can_move(pac_man, right_turn(next_dir)):
                next_dir = find_closest(next_dir, target_coord)
            if not maze.can_move(pac_man, next_dir):
                next_dir = random.choice([left_turn(next_dir), right_turn(next_dir)])

        # if in a dead end, flip direction
        if not (maze.can_move(pac_man, next_dir)) \
                and not (maze.can_move(pac_man, left_turn(next_dir))) \
                and not (maze.can_move(pac_man, right_turn(next_dir))):
            next_dir = left_turn(left_turn(next_dir))


        #print(possible_dirs)
        return next_dir

"""
                # Only attempt turn if more than 1 tick since last turn
                if self.turn_timer > 2:
                    # Run away from the player if it is visible
                    # If it is able to continue in the direction it is facing it will
                    # do so, so long as it does not go towards the player
                    if see_player:
                        if self.look_dir == player_dir or not maze.can_move(self, self.look_dir):
                            self.look_dir = random.choice([left_turn(left_turn(player_dir)),
                                                           left_turn(player_dir), right_turn(player_dir)])
                            self.turn_timer = 0
                    # if player not visible, pick a random movement direction
                    else:
                        self.look_dir = random.choice([self.move_dir, left_turn(self.move_dir),
                                                       right_turn(self.move_dir)])
                        self.turn_timer = 0


            # set target position based on current behaviour
            if self.mode == "normal":
                # Immediately exit house
                if self.array_coord == [house_x, house_y]:
                    target_coord = [house_x, house_y-2]
                elif self.array_coord in([house_x, house_y-1], [house_x, house_y-2]) and self.move_dir == UP:
                    target_coord = [house_x-1, house_y-2]
                # Scatter
                elif (tick_counter / 60) % (self.chase_time + self.scatter_time) < self.scatter_time:
                    target_coord = self.scatter_coord
                # Chase Pac-Man
                else:

            # if dead, move back to ghost house
            elif self.mode == "dead":
                target_coord = [house_x, house_y]

            # move towards target, only attempt a turn at an intersection
            if step < self.x % block_size < block_size - step \
                    and step < self.y % block_size < block_size - step and self.turn_timer > 2:
                if maze.can_move(self, left_turn(self.look_dir)) \
                        or maze.can_move(self, right_turn(self.look_dir)):
                    self.look_dir = find_closest(self.look_dir, target_coord)
                    self.turn_timer = 0
                if not maze.can_move(self, self.look_dir):
                    self.look_dir = random.choice([left_turn(self.move_dir), right_turn(self.move_dir)])
                    self.turn_timer = 0

            # change move direction to match look direction if possible
            if self.look_dir != self.move_dir:
                if maze.can_move(self, self.look_dir):
                    self.move_dir = self.look_dir
                # if in a dead end, flip direction
                if not (maze.can_move(self, self.move_dir)) \
                        and not (maze.can_move(self, left_turn(self.move_dir))) \
                        and not (maze.can_move(self, right_turn(self.move_dir))):
                    self.look_dir = left_turn(left_turn(self.move_dir))
                    self.move_dir = self.look_dir

            # do movement
            if maze.can_move(self, self.move_dir):
                self.x += step * self.COORD_DIR[self.move_dir][0]
                self.y += step * self.COORD_DIR[self.move_dir][1]

        # If outside maze, keep moving forwards until wrapped to the other side of the screen
        else:
            if self.move_dir == LEFT:
                self.x -= self.step_len
                maze.center(self, "y", self.y)
            if self.move_dir == RIGHT:
                self.x += self.step_len
                maze.center(self, "y", self.y)
            # screen wrap
            if self.x < -self.size:
                self.x = display_width
            if self.x > self.size + display_width:
                self.x = -self.size

        # respawn if way found back to house
        if self.mode == "dead" and self.array_coord == [house_x, house_y]:
            self.mode = "normal"

        self.turn_timer += 1

    # Ghost stays in the house and paces left and right
    elif self.mode == "house":
        if self.look_dir == DOWN or self.look_dir == UP:
            self.look_dir = random.choice([LEFT, RIGHT])
            self.move_dir = self.look_dir
        if not (maze.can_move(self, self.move_dir)):
            self.look_dir = left_turn(left_turn(self.move_dir))
            self.move_dir = self.look_dir
        self.x += step * self.COORD_DIR[self.move_dir][0]
        """
