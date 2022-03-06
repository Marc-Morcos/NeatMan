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
import random

#returns grid index for 1D array
def gridToArray(x,y,rowSize=MapSizeX):
    return y*rowSize+x

#Process the inputs for the nead model 
#just passing in everything (SET inputs IN neatConfig to 913)
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
    inputs = np.append(inputs,[pacman.x, pacman.y, pacman.move_dir, pacman.powered_up, (pacman.power_time - pacman.timer),(pacman.lives)])

    return inputs    

#Process the inputs for the nead model 
#this gives the input a grid, 
# with pacman in the center (SET inputs IN neatConfig to camera size(*2 if seperateGhostCam) + 44)
# def cameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit):
#     cameraSizex = 10 #MUST BE ODD NUMBER
#     cameraSizey = 10 #MUST BE ODD NUMBER
#     seperateGhostCam = False
#     cameraRadiusx = int((cameraSizex-1)/2)
#     cameraRadiusy = int((cameraSizey-1)/2)
#     if(seperateGhostCam):
#         inputsSize = 2*cameraSizex*cameraSizey+ 44
#     else:
#         inputsSize = cameraSizex*cameraSizey+ 44
#     inputs = np.zeros(inputsSize)
#     fullGrid = np.zeros((MapSizeX, MapSizeY))

#     ghostvalue = -3 #set in multiple places in the code (avoid changing)
#     blueghostvalue =4
#     wallValue = -1
#     pelletValue = 1
#     PowerPelletValue = 3
#     ghostMoveValue = -4 #set in multiple places in the code (avoid changing)
#     blueGhostMoveValue = 5
#     fruitValue = 2

#     #get pacman true position
#     x = pacman.x-block_size/2.0 
#     y = pacman.y-block_size/2.0
#     truePos = [int(((x)/block_size)),  int(((y)/block_size))]
#     if(truePos[0]>=MapSizeX):
#         truePos[0] = MapSizeX-1
#     if(truePos[1]>=MapSizeY):
#         truePos[1] = MapSizeY-1
#     if(truePos[0]<0):
#         truePos[0] = 0
#     if(truePos[1]<0):
#         truePos[1] = 0

#     #camera offsets from packman
#     cameraMin = [truePos[0]-cameraRadiusx,truePos[1]-cameraRadiusx]
#     cameraMax = [truePos[0]+cameraRadiusy,truePos[1]+cameraRadiusy]

#     #the order in which we add these is important since multiple things can be in the same spot

#     #add visible pellets to the grid
#     for pellet in pellets:
#         if pellet.here:
#             fullGrid[pellet.array_coord[0], pellet.array_coord[1]] = pelletValue

#     #add visible power pellets to the grid
#     for powerPellet in power_pellets:
#         if powerPellet.here:
#             fullGrid[powerPellet.array_coord[0], powerPellet.array_coord[1]] = PowerPelletValue

#     #add visible fruit to the grid
#     if fruit.here:
#         fullGrid[fruit.array_coord[0], fruit.array_coord[1] ] = fruitValue

#     #add ghosts to the grid
#     for ghost in ghosts.values():
#             if(turnOffGhosts): break #make disabled ghosts invisible to model
#             if(ghost.mode != "normal"): continue #hide invisible ghosts

#             x = ghost.x-block_size/2.0 #get the top left corner
#             y = ghost.y-block_size/2.0
#             testTile = [int(x/block_size),  int(y/block_size)]

#             if(testTile[0]>=MapSizeX):
#                 testTile[0] = MapSizeX-1
#             if(testTile[1]>=MapSizeY):
#                 testTile[1] = MapSizeY-1
#             if(testTile[0]<0):
#                 testTile[0] = 0
#             if(testTile[1]<0):
#                 testTile[1] = 0

#             #move direction
#             movecoord = 0
#             if(ghost.move_dir == UP): movecoord = [testTile[0], testTile[1]-1]
#             if(ghost.move_dir == DOWN): movecoord = [testTile[0], testTile[1]+1]
#             if(ghost.move_dir == LEFT): movecoord = [testTile[0]-1, testTile[1]]
#             if(ghost.move_dir == RIGHT): movecoord = [testTile[0]+1, testTile[1]]
#             if(movecoord[0]>=0 and movecoord[0]<MapSizeX and movecoord[1]>=0 and movecoord[1]<MapSizeY and fullGrid[movecoord[0],movecoord[1]]!=wallValue):
#                 fullGrid[movecoord[0],movecoord[1]] = ghostMoveValue
#                 if(ghost.blue): fullGrid[movecoord[0],movecoord[1]] = blueGhostMoveValue

#             fullGrid[testTile[0], testTile[1]] = ghostvalue
#             if(ghost.blue): fullGrid[testTile[0], testTile[1]] = blueghostvalue

#      #populate the inputs array with the local camera
#     for x in range(cameraSizex):
#         if((not wrapAround) and (cameraMin[0]+x<0 or cameraMin[0]+x>=MapSizeX)): continue
#         offset = 0 #wrap screen effect horizontally to account for teleporters
#         while(cameraMin[0]+x+offset<0): offset+=MapSizeX
#         while(cameraMin[0]+x+offset>=MapSizeX): offset-=MapSizeX
#         for y in range(cameraSizey):
#             if(cameraMin[1]+y>=0 and cameraMin[1]+y<MapSizeY):
#                 value = fullGrid[cameraMin[0]+x+offset,cameraMin[1]+y]
#                 if(seperateGhostCam and (value == ghostvalue or value == blueghostvalue or value == ghostMoveValue or value == blueGhostMoveValue)): 
#                     inputs[cameraSizex*cameraSizey+ gridToArray(x, y, cameraSizex)] = value
#                 elif(seperateGhostCam and value == wallValue):
#                     inputs[gridToArray(x, y, cameraSizex)] = value
#                     inputs[cameraSizex*cameraSizey+gridToArray(x, y, cameraSizex)] = value
#                 else:
#                     inputs[gridToArray(x, y, cameraSizex)] = value

#     # #prints camera
#     # tiles = list(inputs)
#     # temp = [(tiles[i:i+cameraSizex]) for i in range(0, len(tiles), cameraSizex)]
#     # for tempRow in temp:
#     #                 print(tempRow)
#     # print("\n\n\n\n\n\n\n")

#     #more ghost info
#     index = cameraSizex*cameraSizey
#     if(seperateGhostCam): index = index*2
#     for ghost in ghosts.values():
#         if(turnOffGhosts): 
#             index+=6
#             continue
#         inputs[index] = ghost.blue
#         index+=1
#         inputs[index] = ghost.move_dir
#         index+=1
#         inputs[index] = (ghost.mode == "normal")
#         index+=1
#         inputs[index] = (pacman.power_time - ghost.blue_timer)
#         index+=1
#         if((pacman.x-ghost.x)!=0 and (ghost.mode == "normal")): inputs[index] = block_size/(pacman.x-ghost.x) #inverted cuz we only care about close ghosts
#         if(ghost.blue): inputs[index] = -inputs[index] #want to get to blue ghosts
#         index+=1
#         if((pacman.y-ghost.y)!=0 and (ghost.mode == "normal")): inputs[index] = block_size/(pacman.y-ghost.y)#inverted cuz we only care about close ghosts
#         if(ghost.blue): inputs[index] = -inputs[index] #want to get to blue ghosts
#         index+=1
    
#     #give distance to a nearest pellet (in case no pellets are on camera)
#     closest = 99999999
#     for pellet in pellets:
#         if pellet.here:
#             xDis = pacman.x-pellet.x
#             yDis = pacman.y-pellet.y
#             distance = abs(xDis) + abs(yDis)
#             if(distance < closest): #no need for pythagoras cuz pacman can't move diagonally
#                 closest = distance
#                 inputs[index] = xDis
#                 inputs[index+1] = yDis
#     index+=2

#     #give ditance to nearest power pellet
#     closest = 99999999
#     for pellet in power_pellets:
#         if pellet.here:
#             xDis = pacman.x-pellet.x
#             yDis = pacman.y-pellet.y
#             distance = abs(xDis) + abs(yDis)
#             if(distance < closest): #no need for pythagoras cuz pacman can't move diagonally
#                 closest = distance
#                 inputs[index] = xDis
#                 inputs[index+1] = yDis
#     index+=2
    
#     #move direction
#     inputs[index+pacman.move_dir] = 1
#     index+=4

#     #more info about pacman
#     inputs[index] = pacman.powered_up
#     index+=1
#     inputs[index] = (pacman.power_time - pacman.timer)
#     index+=1
#     inputs[index] = (pacman.lives)
#     index+=1
#     inputs[index] = (pacman.x)/block_size
#     index+=1
#     inputs[index] = (pacman.y)/block_size
#     index+=1
#     if(fruit.here):
#         inputs[index] = (pacman.y-fruit.y)/block_size
#         index+=1
#         inputs[index] = (pacman.x-fruit.x)/block_size
#     else:
#         inputs[index] = 0
#         index+=1
#         inputs[index] = 0
#     index+=1
#     inputs[index] = fruit.here
#     index+=1

#     #valid moves
#     posX = truePos[0]+1
#     posY = truePos[1]+1
#     if(posX>=0 and posX<MapSizeX and posY>=0 and posY<MapSizeY):
#         inputs[index] = (fullGrid[posX,posY] == -1)
#     else:
#         inputs[index] = False
#     index+=1
    
#     posX = truePos[0]-1
#     posY = truePos[1]+1
#     if(posX>=0 and posX<MapSizeX and posY>=0 and posY<MapSizeY):
#         inputs[index] = (fullGrid[posX,posY] == -1)
#     else:
#         inputs[index] = False
#     index+=1

#     posX = truePos[0]+1
#     posY = truePos[1]-1
#     if(posX>=0 and posX<MapSizeX and posY>=0 and posY<MapSizeY):
#         inputs[index] = (fullGrid[posX,posY] == -1)
#     else:
#         inputs[index] = False
#     index+=1

#     posX = truePos[0]-1
#     posY = truePos[1]-1
#     if(posX>=0 and posX<MapSizeX and posY>=0 and posY<MapSizeY):
#         inputs[index] = (fullGrid[posX,posY] == -1)
#     else:
#         inputs[index] = False
#     index+=1

#     return inputs


#Process the inputs for the nead model 
#this gives the input a grid, 
# with pacman in the center (SET inputs IN neatConfig to camera size(*2 if seperateGhostCam) + 0)
def rotatingCameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit):
    cameraSize = 3 #MUST BE ODD NUMBER
    cameraRadius = int((cameraSize-1)/2)
    fullGrid = np.zeros((MapSizeX, MapSizeY))
    
    ghostvalue = -3 
    blueghostvalue = 4
    wallValue = -1
    pelletValue = 1
    PowerPelletValue = 3
    ghostMoveValue = -4 
    blueGhostMoveValue = 5
    fruitValue = 2

    # ghostvalue = 5 #set in multiple places in the code (avoid changing)
    # blueghostvalue =7
    # wallValue = 2
    # pelletValue = 1
    # PowerPelletValue = 3
    # ghostMoveValue = 6 #set in multiple places in the code (avoid changing)
    # blueGhostMoveValue = 4
    # fruitValue = 8

    #get pacman true position
    x = pacman.x-block_size/2.0 
    y = pacman.y-block_size/2.0
    truePos = [int(((x)/block_size)),  int(((y)/block_size))]
    if(truePos[0]>=MapSizeX):
        truePos[0] = MapSizeX-1
    if(truePos[1]>=MapSizeY):
        truePos[1] = MapSizeY-1
    if(truePos[0]<0):
        truePos[0] = 0
    if(truePos[1]<0):
        truePos[1] = 0

    #camera offsets from pacqman
    cameraMin = [truePos[0]-cameraRadius,truePos[1]-cameraRadius]
    cameraMax = [truePos[0]+cameraRadius,truePos[1]+cameraRadius]

    #the order in which we add these is important since multiple things can be in the same spot

    #add visible pellets to the grid
    for pellet in pellets:
        if pellet.here:
            fullGrid[pellet.array_coord[0], pellet.array_coord[1]] = pelletValue

    #add visible power pellets to the grid
    for powerPellet in power_pellets:
        if powerPellet.here:
            fullGrid[powerPellet.array_coord[0], powerPellet.array_coord[1]] = PowerPelletValue

    #add visible fruit to the grid
    if fruit.here:
        fullGrid[fruit.array_coord[0], fruit.array_coord[1] ] = fruitValue

    #add visible walls to the grid
    for wall in maze.wall_locs:
        fullGrid[wall[0], wall[1]] = wallValue
    for wall in maze.ghost_door_locs: #ghost doors are basically walls
        fullGrid[wall[0], wall[1]] = wallValue
        
    #add ghosts to the grid
    for ghost in ghosts.values():
            if(turnOffGhosts): break #make disabled ghosts invisible to model
            if(ghost.mode != "normal"): continue #hide invisible ghosts

            x = ghost.x-block_size/2.0 #get the top left corner
            y = ghost.y-block_size/2.0
            testTile = [int(x/block_size),  int(y/block_size)]

            if(testTile[0]>=MapSizeX):
                testTile[0] = MapSizeX-1
            if(testTile[1]>=MapSizeY):
                testTile[1] = MapSizeY-1
            if(testTile[0]<0):
                testTile[0] = 0
            if(testTile[1]<0):
                testTile[1] = 0

            #move direction
            movecoord = 0
            if(ghost.move_dir == UP): movecoord = [testTile[0], testTile[1]-1]
            if(ghost.move_dir == DOWN): movecoord = [testTile[0], testTile[1]+1]
            if(ghost.move_dir == LEFT): movecoord = [testTile[0]-1, testTile[1]]
            if(ghost.move_dir == RIGHT): movecoord = [testTile[0]+1, testTile[1]]
            if(movecoord[0]>=0 and movecoord[0]<MapSizeX and movecoord[1]>=0 and movecoord[1]<MapSizeY and fullGrid[movecoord[0],movecoord[1]]!=wallValue):
                fullGrid[movecoord[0],movecoord[1]] = ghostMoveValue
                if(ghost.blue): fullGrid[movecoord[0],movecoord[1]] = blueGhostMoveValue

            fullGrid[testTile[0], testTile[1]] = ghostvalue
            if(ghost.blue): fullGrid[testTile[0], testTile[1]] = blueghostvalue

    smallCamera = np.zeros((cameraSize, cameraSize))

     #populate the inputs array with the local camera
    for x in range(cameraSize):
        if((not wrapAround) and (cameraMin[0]+x<0 or cameraMin[0]+x>=MapSizeX)): continue
        offset = 0 #wrap screen effect horizontally to account for teleporters
        while(cameraMin[0]+x+offset<0): offset+=MapSizeX
        while(cameraMin[0]+x+offset>=MapSizeX): offset-=MapSizeX
        for y in range(cameraSize):
            if(cameraMin[1]+y>=0 and cameraMin[1]+y<MapSizeY):
                smallCamera[y, x] = fullGrid[cameraMin[0]+x+offset,cameraMin[1]+y]
    
    #rotation based on pacman's move_dir
    if pacman.move_dir == RIGHT:
        smallCamera = np.rot90(smallCamera, 1)
    elif pacman.move_dir == DOWN:
        smallCamera = np.rot90(smallCamera, 2)
    elif pacman.move_dir == LEFT:
        smallCamera = np.rot90(smallCamera, 3)
    
    inputs = smallCamera.reshape(-1)
    
    # #prints camera
    # tiles = list(inputs)
    # temp = [(tiles[i:i+cameraSize]) for i in range(0, len(tiles), cameraSize)]
    # for tempRow in temp:
    #                 print(tempRow)
    # print("\n\n\n\n\n\n\n")
    

    return inputs  

#nead model controller
def modelNeat(pacman, maze, ghosts, pellets, power_pellets, fruit):

    ghostMoveValue = -4 #set in multiple places in the code (avoid changing)
    
    #Get the inputs
    inputs = rotatingCameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit)

    #pass inputs into the neural network
    outputs = pacman.net.activate(inputs)

    nextMove = 0
    
    #interpret net output 
    # if(len(outputs) == 4):
    #     max = outputs[0]
    #     max_ids = [0]
    #     for output_id in range(1,len(outputs)):
    #         if outputs[output_id] > max:
    #             max = outputs[output_id]
    #             max_ids = [output_id]
    #         elif outputs[output_id] == max:
    #             max_ids.append(output_id)
    #     nextMove = random.choice(max_ids) 

    if(len(outputs) == 2):
            #interpret net output 
            if(abs(outputs[0]) > abs(outputs[1])):
                axis = 0
            else:
                axis = 1
            
            if(outputs[axis]>0):
                if(axis == 0):
                    nextMove = pacman.move_dir
                else:
                    nextMove = pacman.move_dir + 1
            else:
                if(axis == 0):
                    nextMove = pacman.move_dir + 2
                else:
                    nextMove =  pacman.move_dir - 1
        
    elif(len(outputs) == 3):
            #interpret net output 
            if(outputs[2]>0):
                axis = 0
            else:
                axis = 1
            
            if(outputs[axis]>0):
                if(axis == 0):
                    nextMove = pacman.move_dir
                else:
                    nextMove = pacman.move_dir + 1
            else:
                if(axis == 0):
                    nextMove = pacman.move_dir + 2
                else:
                    nextMove = pacman.move_dir -1


    nextMove = nextMove%4        
            
    return nextMove

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

#a custom hit ditection function
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
    # rotatingCameraNeatHelper(pac_man, maze, ghosts, pellets, power_pellets, fruit)

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
                #print("AHHH ghost at ({},{}) in direction {}".format(testTile[0],testTile[1], direction))
                possible_dirs.remove(direction)
                break

    if len(possible_dirs) != 0 and (pac_man.oldPosDir != possible_dirs or not pac_man.move_dir in possible_dirs):
        pac_man.oldPosDir = copy.deepcopy(possible_dirs)
        return random.choice(possible_dirs)
    return pac_man.move_dir

# A queue node used in BFS -> taken and adapted from https://www.techiedelight.com/find-shortest-path-source-destination-matrix-satisfies-given-constraints/
class queueNode:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def getPath(node, path):
    if node:
        getPath(node.parent, path)
        path.append(node)

def find_path_to_objective(start, objective, blocked, mazeArray):

    start = queueNode(start[0], start[1])

    queue = list()
    visited = set()

    visited.add((start.x,start.y))

    queue.append(start)

    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))

    while queue:

        curr = queue.pop(0)
        
        if [curr.x, curr.y] in objective:
            path = []
            getPath(curr, path)
            return path

        #check adjacents and add to queue
        for testX, testY in dirs:
                x = (testX+curr.x)%len(mazeArray[0])
                y = (testY+curr.y)%len(mazeArray)

                if(not mazeArray[y][x] in blocked):
                    nextCoord = queueNode(x,y, curr)
                    if (nextCoord.x,nextCoord.y) not in visited:
                        queue.append(nextCoord)
                        visited.add((nextCoord.x,nextCoord.y))

    return -1

#the final baseline level -> able to path find to a variety of targets such as pellets or blue ghosts 
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

    # Don't get power pellets until all ghosts are active
    if ghosts["clyde"].mode == "normal":
        blocked = [1,3]
    else:
        blocked = [1,3,4]

    path = -1
    timed_objectives = []

    #path finder 
    if pac_man.powered_up and pac_man.ghosts_eaten < 4:
        for ghost in ghosts.values():
            if ghost.mode == "normal" and ghost.blue:
                timed_objectives.append(ghost.array_coord)      
    
    if fruit.here:
        timed_objectives.append(fruit.array_coord)

    if timed_objectives:
        path = find_path_to_objective([pac_manX, pac_manY], timed_objectives, blocked, mazeArray)
    
    if path == -1:
        power_pellet_locs = []
        for power_pellet in power_pellets:
            if power_pellet.here:
                power_pellet_locs.append(power_pellet.array_coord)

        if power_pellet_locs and ghosts["clyde"].mode == "normal":
            path = find_path_to_objective([pac_manX, pac_manY], power_pellet_locs, blocked, mazeArray)

        if path == -1:
            pellet_locs = []
            for pellet in pellets:
                if pellet.here:
                    pellet_locs.append(pellet.array_coord)
            path = find_path_to_objective([pac_manX, pac_manY], pellet_locs, blocked, mazeArray)

    #if no path is avaliable panic
    if(path == -1):
        return avoid_ghost_and_wall_dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit)
    elif len(path) < 2:
        return pac_man.move_dir
    else:
        nextTile = [path[1].x, path[1].y]
        if(nextTile[0]>pac_manX): return RIGHT
        if(nextTile[0]<pac_manX): return LEFT
        if(nextTile[1]>pac_manY): return DOWN
        if(nextTile[1]<pac_manY): return UP



