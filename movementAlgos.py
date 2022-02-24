import random
from re import L, X
from turtle import down, right
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from operator import *
import math
from Pac_Man import Pac_Man
import numpy as np
import copy
from collections import deque

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

def printMaze(maze):
    for y in range(len(maze)):
        row = " "
        for x in range(len(maze[0])):
            row += str(maze[y][x]) + " "
        print(row)

#random moves -> no smart
def dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pac_man.move_dir

def betterCanMove(entity, mazeArray, direction):

    blocked = [1,3]
    horzMov = [LEFT, RIGHT]
    vertMov = [UP, DOWN]


    x = entity.x-block_size/2.0 #get the top left corner
    y = entity.y-block_size/2.0

    occupiedTiles = [[int(round((x)/block_size)),  int(round((y)/block_size))]] 

    for textX in range(0,2):
        for textY in range(0,2):
            testTileX = int(((x + textX * (block_size - 1))/block_size))
            testTileY = int(((y + textY * (block_size - 1))/block_size))
            testTile = [testTileX,testTileY]
            if(not testTile in occupiedTiles) and testTileX>=occupiedTiles[0][0]  and testTileY>=occupiedTiles[0][1]:
                occupiedTiles.append(testTile)

    #determine if its in motion 
    if len(occupiedTiles) == 2:
        if(occupiedTiles[0][0] == occupiedTiles[1][0] and direction in vertMov):
            return True
        elif(occupiedTiles[0][1] == occupiedTiles[1][1] and direction in horzMov):
            return True


    deltaX,deltaY = entity.COORD_DIR[direction]
     
    for tileX, tileY in occupiedTiles:
        #print("Testing: ({},{}){} Data: {}".format(tileX, tileY, direction, mazeArray[tileY+deltaY][tileX+deltaX]))

        if mazeArray[(tileY+deltaY)%len(mazeArray)][(tileX+deltaX)%len(mazeArray[0])] in blocked:
            return False

    return True
    
#human controlled pac_man
def humanPlayer(pac_man, maze, ghosts, pellets, power_pellets, fruit):

    x = pac_man.x-block_size/2.0 #get the top left corner
    y = pac_man.y-block_size/2.0

    occupiedTiles = [[int(round((x)/block_size)),  int(round((y)/block_size))]] 

    for textX in range(0,2):
        for textY in range(0,2):
            testTileX = int(((x + textX * (block_size - 1))/block_size))
            testTileY = int(((y+ textY * (block_size - 1))/block_size))
            testTile = [testTileX,testTileY]
            if(not testTile in occupiedTiles) and testTileX>=occupiedTiles[0][0]  and testTileY>=occupiedTiles[0][1]:
                occupiedTiles.append(testTile)
    

    #print(occupiedTiles)
    possible_dirs = []

    if(betterCanMove(pac_man, maze.maze_array, RIGHT)):
        possible_dirs.append(RIGHT)

    if(betterCanMove(pac_man, maze.maze_array, LEFT)):
        possible_dirs.append(LEFT)

    if(betterCanMove(pac_man, maze.maze_array, UP)):
        possible_dirs.append(UP)

    if(betterCanMove(pac_man, maze.maze_array, DOWN)):
        possible_dirs.append(DOWN)

    return pac_man.humanInput

#moves randomly but does not run into walls or ghosts 
def avoid_ghost_and_wall_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    #evaluate walls 
    possible_dirs = []

    if(betterCanMove(pac_man, maze.maze_array, RIGHT)):
        possible_dirs.append(RIGHT)

    if(betterCanMove(pac_man, maze.maze_array, LEFT)):
        possible_dirs.append(LEFT)

    if(betterCanMove(pac_man, maze.maze_array, UP)):
        possible_dirs.append(UP)

    if(betterCanMove(pac_man, maze.maze_array, DOWN)):
        possible_dirs.append(DOWN)

    ghostTiles = []

    for ghost in ghosts.values():
        if ghost.mode == "normal" and ghost.blue == False:
            x = ghost.x-block_size/2.0 #get the top left corner
            y = ghost.y-block_size/2.0

            for textX in range(0,2):
                for textY in range(0,2):
                    testTile = [int(((x + textX * (block_size - 1))/block_size)),  int(((y+ textY * (block_size - 1))/block_size))]
                    if(not testTile in ghostTiles):
                        ghostTiles.append(testTile)


    pac_manTiles = []
    x = pac_man.x-block_size/2.0 #get the top left corner
    y = pac_man.y-block_size/2.0

    for textX in range(0,2):
        for textY in range(0,2):
            testTile = [int(((x + textX * (block_size - 1))/block_size)),  int(((y+ textY * (block_size - 1))/block_size))]
            if(not testTile in pac_manTiles):
                pac_manTiles.append(testTile)


    for direction in possible_dirs:
        testRange = 2
        deltaX,deltaY = pac_man.COORD_DIR[direction]

        tiles_to_test = []
        for tileX, tileY in pac_manTiles:
            for i in range(1, testRange+1):
                if(i==1 and deltaX == 0):
                    for cornercheck in range(-1,2):
                        testTile = [tileX+deltaX*i + cornercheck, tileY+deltaY*i]
                        if not testTile in tiles_to_test:
                            tiles_to_test.append(testTile)

                if(i==1 and deltaY == 0):
                    for cornercheck in range(-1,2):
                        testTile = [tileX+deltaX*i, tileY+deltaY*i+ cornercheck]
                        if not testTile in tiles_to_test:
                            tiles_to_test.append(testTile)

                else: 
                    testTile = [tileX+deltaX*i, tileY+deltaY*i]
                    if not testTile in tiles_to_test:
                        tiles_to_test.append(testTile)

        for testTile in tiles_to_test:
            if(testTile in ghostTiles):
                print("AHHH ghost at ({},{}) in direction {}".format(testTile[0],testTile[1], direction))
                possible_dirs.remove(direction)
                break


    if len(possible_dirs) != 0 and (pac_man.oldPosDir != possible_dirs or not pac_man.move_dir in possible_dirs):
        pac_man.oldPosDir = copy.deepcopy(possible_dirs)
        return random.choice(possible_dirs)
    return pac_man.move_dir

# A queue node used in BFS -> taken and adapted from https://www.techiedelight.com/find-shortest-path-source-destination-matrix-satisfies-given-constraints/
class queueNode:
    # (x, y) represents coordinates of a cell in the matrix
    # maintain a parent node for the printing path
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def getPath(node, path):
    if node:
        getPath(node.parent, path)
        path.append(node)


def findPath(start, end, mazeArray):

    start = queueNode(start[0], start[1])
    end   = queueNode(end[0], end[1])
    
    blocked = [1,3]

    if mazeArray[start.y][start.x] in blocked or mazeArray[end.y][end.x] in blocked:
        return -1

    queue = deque()
    visited = set()

    visited.add((start.x,start.y))

    queue.append(start)

    while queue:

        curr = queue.popleft() 
         
        if curr.x == end.x and curr.y == end.y:
            path = []
            getPath(curr, path)
            return path
        
        #check adjacents and add to queue
        for testX in range(-1, 2):
            for testY in range(-1, 2):

                x = (testX+curr.x)%len(mazeArray[0])
                y = (testY+curr.y)%len(mazeArray)

                if(not mazeArray[y][x] in blocked):
                    nextCoord = queueNode(x,y, curr)
                    if (nextCoord.x,nextCoord.y) not in visited:
                        queue.append(nextCoord)
                        visited.add((nextCoord.x,nextCoord.y))

    return -1


def pathFind_to_target(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    mazeArray = copy.deepcopy(maze.maze_array)

    #makes hostile ghosts appear as walls to the path finding algo
    for ghost in ghosts.values():
        if ghost.mode == "normal" and ghost.blue == False:
            x = ghost.x-block_size/2.0 #get the top left corner
            y = ghost.y-block_size/2.0

            for textX in range(0,2):
                for textY in range(0,2):
                    mazeArray[int(((y+ textY * (block_size - 1))/block_size))%len(mazeArray)][int(((x + textX * (block_size - 1))/block_size))%len(mazeArray[0])] = 1

                   
    pac_manX = int(round((pac_man.x-block_size/2.0)/block_size))%len(mazeArray[0]) #get pacman location
    pac_manY = int(round((pac_man.y-block_size/2.0)/block_size))%len(mazeArray) 

    target_tile = [1,1] # colin add your funky fresh function   
    
    path = findPath([pac_manX, pac_manY], target_tile, mazeArray)
    
    #if no path is avaliable panic
    if(path == -1 or len(path)<2):
        return avoid_ghost_and_wall_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit)

    else:
        nextTile = [path[1].x, path[1].y]
        if(nextTile[0]>pac_manX): return RIGHT
        if(nextTile[0]<pac_manX): return LEFT
        if(nextTile[1]>pac_manY): return DOWN
        if(nextTile[1]<pac_manY): return UP




""" old code ahhhh nothing works 
#avoid ghosts
def avoid_ghost_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    avoid_distance = 100
    possible_dirs = set([RIGHT, LEFT, UP, DOWN])

    for ghost in ghosts.values():
        :
            # Remove directions that are near an active ghost
            if 0 < ghost.array_coord[0] - pac_man.array_coord[0] < avoid_distance:
               possible_dirs -= set([RIGHT])

            if 0 < pac_man.array_coord[0] - ghost.array_coord[0] < avoid_distance:
                possible_dirs -= set([LEFT])

            if 0 < ghost.array_coord[1] - pac_man.array_coord[1] < avoid_distance:
               possible_dirs -= set([DOWN])

            if 0 < pac_man.array_coord[1] - ghost.array_coord[1] < avoid_distance:
                possible_dirs -= set([UP])

    # Select a random direction out of the possible directions
    if possible_dirs:
        next_dir = random.sample(possible_dirs, 1)[0]
        print(possible_dirs)
        print(next_dir)
        return 
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

""""""
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
