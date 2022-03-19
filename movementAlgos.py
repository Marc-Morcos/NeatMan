import random
from re import L, X
from tkinter import Y
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

#    soroundings = [0,0,0,0]
#     if(truePos[0]+1 < MapSizeX): #right
#         soroundings[0] = fullGrid[truePos[0]+1,truePos[1]]
#     if(truePos[0]-1 >= 0): #left
#         soroundings[1] = fullGrid[truePos[0]-1,truePos[1]]
#     if(truePos[1]+1 < MapSizeY): #down
#         soroundings[2] = fullGrid[truePos[0],truePos[1]+1]
#     if(truePos[1]-1 >= 0): #up
#         soroundings[3] = fullGrid[truePos[0],truePos[1]-1]

#     return inputs, soroundings  


def rotatingCameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit):
   
    #get pacman true position
    x = pacman.x-block_size/2.0 
    y = pacman.y-block_size/2.0
    truePos2 = [(((x)/block_size)),  (((y)/block_size))]

    if block_size < pacman.x < MapSizeX* block_size - block_size:
        canmove = np.array([[maze.can_move(pacman, UP)==True,maze.can_move(pacman, RIGHT)==True],[maze.can_move(pacman, LEFT)==True,maze.can_move(pacman, DOWN)==True]])
    else:
        canmove = np.array([[False,False],[False,False]])

    canmove2 = np.array([[betterCanMove(pacman, maze.maze_array, UP)==True,betterCanMove(pacman, maze.maze_array, RIGHT)==True],[betterCanMove(pacman, maze.maze_array, LEFT)==True,betterCanMove(pacman, maze.maze_array, DOWN)==True]])


    #sensing
    closeGhosts = np.array([[6,6],[6,6]],dtype=float)
    closeGhosts2 = np.array([[6,6],[6,6]],dtype=float)
    for ghost in ghosts.values():
        if(turnOffGhosts or (ghost.blue and not (ghost.blue_timer + (30) >= pacman.power_time)) or ghost.mode != "normal"): continue
        x = ghost.x-block_size/2.0 #get the top left corner
        y = ghost.y-block_size/2.0
        testTile = [(x/block_size),  (y/block_size)]
        distx = testTile[0]-truePos2[0]
        disty = testTile[1]-truePos2[1]
        totalDist = abs(distx)+abs(disty)
        totalDist = totalDist/5
        if(disty<0 and totalDist<closeGhosts[0,0]):
            closeGhosts[0,0] = totalDist
        if(disty>0 and totalDist<closeGhosts[1,1]):
            closeGhosts[1,1] = totalDist
        if(distx<0 and totalDist<closeGhosts[1,0]):
            closeGhosts[1,0] =totalDist
        if(distx>0 and totalDist<closeGhosts[0,1]):
            closeGhosts[0,1] = totalDist
        
        if(disty<0 and abs(distx) ==0 and canmove2[0,0] and totalDist<closeGhosts2[0,0]):
            closeGhosts2[0,0] = totalDist
        if(disty>0 and abs(distx) ==0 and canmove2[1,1] and totalDist<closeGhosts2[1,1]):
            closeGhosts2[1,1] = totalDist
        if(distx<0 and abs(disty) ==0 and canmove2[1,0] and totalDist<closeGhosts2[1,0]):
            closeGhosts2[1,0] =totalDist
        if(distx>0 and abs(disty) ==0 and canmove2[0,1] and totalDist<closeGhosts2[0,1]):
            closeGhosts2[0,1] = totalDist

    closeBlueGhosts = np.array([[6,6],[6,6]],dtype=float)
    closeBlueGhosts2 = np.array([[6,6],[6,6]],dtype=float)
    for ghost in ghosts.values():
        if(turnOffGhosts or (not ghost.blue or (ghost.blue_timer + (30) >= pacman.power_time)) or ghost.mode != "normal"): continue
        x = ghost.x-block_size/2.0 #get the top left corner
        y = ghost.y-block_size/2.0
        testTile = [(x/block_size),  (y/block_size)]
        distx = testTile[0]-truePos2[0]
        disty = testTile[1]-truePos2[1]
        totalDist = abs(distx)+abs(disty)
        totalDist = totalDist/5
        if(disty<0 and totalDist<closeBlueGhosts[0,0]):
            closeBlueGhosts[0,0] = totalDist
        if(disty>0 and totalDist<closeBlueGhosts[1,1]):
            closeBlueGhosts[1,1] = totalDist
        if(distx<0 and totalDist<closeBlueGhosts[1,0]):
            closeBlueGhosts[1,0] = totalDist
        if(distx>0 and totalDist<closeBlueGhosts[0,1]):
            closeBlueGhosts[0,1] = totalDist
        
        if(disty<0 and abs(distx) ==0 and canmove2[0,0] and totalDist<closeBlueGhosts2[0,0]):
            closeBlueGhosts2[0,0] = totalDist
        if(disty>0 and abs(distx) ==0 and canmove2[1,1] and totalDist<closeBlueGhosts2[1,1]):
            closeBlueGhosts2[1,1] = totalDist
        if(distx<0 and abs(disty)  ==0 and canmove2[1,0] and totalDist<closeBlueGhosts2[1,0]):
            closeBlueGhosts2[1,0] = totalDist
        if(distx>0 and abs(disty) ==0 and canmove2[0,1] and totalDist<closeBlueGhosts2[0,1]):
            closeBlueGhosts2[0,1] = totalDist

    #add fruit to blue ghosts
    if fruit.here:
        distx = fruit.array_coord[0]-truePos2[0]
        disty = fruit.array_coord[1]-truePos2[1]
        totalDist = abs(distx)+abs(disty)
        totalDist = totalDist/5
        if(disty<0 and totalDist<closeBlueGhosts[0,0]):
            closeBlueGhosts[0,0] = totalDist
        if(disty>0 and totalDist<closeBlueGhosts[1,1]):
            closeBlueGhosts[1,1] = totalDist
        if(distx<0 and totalDist<closeBlueGhosts[1,0]):
            closeBlueGhosts[1,0] = totalDist
        if(distx>0 and totalDist<closeBlueGhosts[0,1]):
            closeBlueGhosts[0,1] = totalDist
        
        if(disty<0 and abs(distx) ==0 and canmove2[0,0] and totalDist<closeBlueGhosts2[0,0]):
            closeBlueGhosts2[0,0] = totalDist
        if(disty>0 and abs(distx) ==0 and canmove2[1,1] and totalDist<closeBlueGhosts2[1,1]):
            closeBlueGhosts2[1,1] = totalDist
        if(distx<0 and abs(disty) ==0 and canmove2[1,0] and totalDist<closeBlueGhosts2[1,0]):
            closeBlueGhosts2[1,0] = totalDist
        if(distx>0 and abs(disty) ==0 and canmove2[0,1] and totalDist<closeBlueGhosts2[0,1]):
            closeBlueGhosts2[0,1] = totalDist

    closePellets = np.array([[6,6],[6,6]],dtype=float)
    closePellets2 = np.array([[6,6],[6,6]],dtype=float)
    for pellet in pellets:
        if not pellet.here: continue
        distx = pellet.array_coord[0]-truePos2[0]
        disty = pellet.array_coord[1]-truePos2[1]
        totalDist = abs(distx)+abs(disty)
        totalDist = totalDist/5
        if(disty<0 and totalDist<closePellets[0,0]):
            closePellets[0,0] =totalDist
        if(disty>0 and totalDist<closePellets[1,1]):
            closePellets[1,1] =totalDist
        if(distx<0 and totalDist<closePellets[1,0]):
            closePellets[1,0] = totalDist
        if(distx>0 and totalDist<closePellets[0,1]):
            closePellets[0,1] = totalDist
        
        if(disty<0 and abs(distx) ==0 and canmove2[0,0] and totalDist<closePellets2[0,0]):
            closePellets2[0,0] =totalDist
        if(disty>0 and abs(distx) ==0 and canmove2[1,1] and totalDist<closePellets2[1,1]):
            closePellets2[1,1] =totalDist
        if(distx<0 and abs(disty) ==0 and canmove2[1,0] and totalDist<closePellets2[1,0]):
            closePellets2[1,0] = totalDist
        if(distx>0 and abs(disty) ==0 and canmove2[0,1] and totalDist<closePellets2[0,1]):
            closePellets2[0,1] = totalDist

    closePowerPellets = np.array([[6,6],[6,6]],dtype=float)
    closePowerPellets2 = np.array([[6,6],[6,6]],dtype=float)
    for powerPellet in power_pellets:
        if not powerPellet.here: continue
        distx = powerPellet.array_coord[0]-truePos2[0]
        disty = powerPellet.array_coord[1]-truePos2[1]
        totalDist = abs(distx)+abs(disty)
        totalDist = totalDist/5
        if(disty<0 and totalDist<closePowerPellets[0,0]):
            closePowerPellets[0,0] = totalDist
        if(disty>0 and totalDist<closePowerPellets[1,1]):
            closePowerPellets[1,1] = totalDist
        if(distx<0 and totalDist<closePowerPellets[1,0]):
            closePowerPellets[1,0] = totalDist
        if(distx>0 and totalDist<closePowerPellets[0,1]):
            closePowerPellets[0,1] = totalDist
        
        if(disty<0 and abs(distx) ==0 and canmove2[0,0] and totalDist<closePowerPellets2[0,0]):
            closePowerPellets2[0,0] = totalDist
        if(disty>0 and abs(distx) ==0 and canmove2[1,1] and totalDist<closePowerPellets2[1,1]):
            closePowerPellets2[1,1] = totalDist
        if(distx<0 and abs(disty) ==0 and canmove2[1,0] and totalDist<closePowerPellets2[1,0]):
            closePowerPellets2[1,0] = totalDist
        if(distx>0 and abs(disty) ==0 and canmove2[0,1] and totalDist<closePowerPellets2[0,1]):
            closePowerPellets2[0,1] = totalDist

    rotateDir = pacman.move_dir
    if (wacky2Output or oneOutput) and (((pacman.look_dir-pacman.move_dir)%4) == 1):
        rotateDir = pacman.look_dir

    if(rotateCamera):
        if rotateDir == RIGHT:
            closeGhosts = np.rot90(closeGhosts, 1).reshape(-1)
            closeBlueGhosts = np.rot90(closeBlueGhosts, 1).reshape(-1)
            closePellets = np.rot90(closePellets, 1).reshape(-1)
            closePowerPellets = np.rot90(closePowerPellets, 1).reshape(-1)
            closeGhosts2 = np.rot90(closeGhosts2, 1).reshape(-1)
            closeBlueGhosts2 = np.rot90(closeBlueGhosts2, 1).reshape(-1)
            closePellets2 = np.rot90(closePellets2, 1).reshape(-1)
            closePowerPellets2 = np.rot90(closePowerPellets2, 1).reshape(-1)
            canmove = np.rot90(canmove, 1).reshape(-1)
            canmove2 = np.rot90(canmove2, 1).reshape(-1)
            
        elif rotateDir == DOWN:
            closeGhosts = np.rot90(closeGhosts, 2).reshape(-1)
            closeBlueGhosts = np.rot90(closeBlueGhosts, 2).reshape(-1)
            closePellets = np.rot90(closePellets, 2).reshape(-1)
            closePowerPellets = np.rot90(closePowerPellets, 2).reshape(-1)
            closeGhosts2 = np.rot90(closeGhosts2, 2).reshape(-1)
            closeBlueGhosts2 = np.rot90(closeBlueGhosts2, 2).reshape(-1)
            closePellets2 = np.rot90(closePellets2, 2).reshape(-1)
            closePowerPellets2 = np.rot90(closePowerPellets2, 2).reshape(-1)
            canmove = np.rot90(canmove, 2).reshape(-1)
            canmove2 = np.rot90(canmove2, 2).reshape(-1)
        elif rotateDir == LEFT:
            closeGhosts = np.rot90(closeGhosts, 3).reshape(-1)
            closeBlueGhosts = np.rot90(closeBlueGhosts, 3).reshape(-1)
            closePellets = np.rot90(closePellets, 3).reshape(-1)
            closePowerPellets = np.rot90(closePowerPellets, 3).reshape(-1)
            closeGhosts2 = np.rot90(closeGhosts2, 3).reshape(-1)
            closeBlueGhosts2 = np.rot90(closeBlueGhosts2, 3).reshape(-1)
            closePellets2 = np.rot90(closePellets2, 3).reshape(-1)
            closePowerPellets2 = np.rot90(closePowerPellets2, 3).reshape(-1)
            canmove = np.rot90(canmove, 3).reshape(-1)
            canmove2 = np.rot90(canmove2, 3).reshape(-1)
        else:
            closeGhosts = closeGhosts.reshape(-1)
            closeBlueGhosts = closeBlueGhosts.reshape(-1)
            closePellets = closePellets.reshape(-1)
            closePowerPellets = closePowerPellets.reshape(-1)
            closeGhosts2 = closeGhosts2.reshape(-1)
            closeBlueGhosts2 = closeBlueGhosts2.reshape(-1)
            closePellets2 = closePellets2.reshape(-1)
            closePowerPellets2 = closePowerPellets2.reshape(-1)
            canmove = canmove.reshape(-1)
            canmove2 = canmove2.reshape(-1)

    inputs = np.concatenate(([pacman.framesNotMoving],closeGhosts,closeBlueGhosts,closePellets,closePowerPellets,closeGhosts2,closeBlueGhosts2,closePellets2,closePowerPellets2,canmove,canmove2))

    # #prints camera
    # tiles = list(inputs)
    # temp = [(tiles[i:i+cameraSize]) for i in range(0, len(tiles), cameraSize)]
    # for tempRow in temp:
    #                 print(tempRow)
    # print("\n\n\n\n\n\n\n")

    return inputs  

#nead model controller
def modelNeat(pacman, maze, ghosts, pellets, power_pellets, fruit):
    
    #Get the inputs
    inputs = rotatingCameraNeatHelper(pacman, maze, ghosts, pellets, power_pellets, fruit)

    #pass inputs into the neural network
    outputs = pacman.net.activate(inputs)

    nextMove = 0
    
    # interpret net output 
    if(oneOutput):
        if(len(outputs)!=1): print("oneOutput on but not 1 output")
        if(outputs[0] >= 0):
                    nextMove = pacman.move_dir #yes I know these don't match, im trying something
        else:
                    nextMove = pacman.look_dir + 1
    
    elif(wacky2Output):
        if(len(outputs)!=2): print("wacky2Outputs on but not 2 outputs")
        if(outputs[0]>0):
            nextMove = pacman.move_dir 
        else:
            if(outputs[1] >= 0):
                    nextMove = pacman.move_dir - 1
            else:
                if ((pacman.look_dir-pacman.move_dir)%4) == 1:
                    nextMove = pacman.look_dir + 1
                else:
                    nextMove = pacman.move_dir + 1


    elif(len(outputs) == 2):
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
    
    elif(len(outputs) == 4):
        maxInd = -1
        maxVal = -9999
        for i in range(4):
            if(outputs[i]>maxVal):
                maxVal = outputs[i]
                maxInd = i

        FourDirs = [pacman.move_dir,pacman.move_dir+1,pacman.move_dir+3,pacman.move_dir+2]
        nextMove = FourDirs[maxInd]

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




