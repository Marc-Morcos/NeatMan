import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
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

def dummy(pacman, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pacman.move_dir

def humanPlayer(pacman, maze, ghosts, pellets, power_pellets, fruit):
    return pacman.humanInput
    