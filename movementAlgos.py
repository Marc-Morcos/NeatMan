import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from Pac_Man import Pac_Man
import numpy as np

def dummy(pacman, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pacman.move_dir

def humanPlayer(pacman, maze, ghosts, pellets, power_pellets, fruit):
    return pacman.humanInput

def neat(pacman, maze, ghosts, pellets, power_pellets, fruit):
    #converting the inputs to a 1D array to pass into NEAT
    inputs = np.array(maze.maze_array)
    inputs = inputs.flatten()
    
    #tell ai about fruit
    inputs.append(fruit.here, fruit.x, fruit.y)

    #tell ai about power pellets
    for power_pellet in power_pellets:
        inputs.append(power_pellet.here, power_pellet.x, power_pellet.y)
    
    #tell ai about ghosts (boo)
    for ghost in ghosts:
        inputs.append(ghost.x, ghost.y, ghost.blue, ghost.move_dir, (ghost.mode == "normal"), (pacman.power_time - ghost.blue_timer))
    
    #tell ai about pacman
    inputs.append(pacman.x, pacman.y, pacman.move_dir, pacman.powered_up, (pacman.power_time - pacman.timer))

    #pass inputs into the neural network
    outputs = pacman.net.activate(inputs)
    
    #interpret net output 
    max = outputs[0]
    for output_id in range(len(outputs)):
        if outputs[output_id] > max:
            max = outputs[output_id]

    return max
    