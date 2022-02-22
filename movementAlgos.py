import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from Pac_Man import Pac_Man

#random moves -> no smart
def dummy(pacman, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pacman.move_dir

#human controlled pacman
def humanPlayer(pacman, maze, ghosts, pellets, power_pellets, fruit):
    return pacman.humanInput

#avoid ghosts and walls
def avoidGhostDummy(pacman, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pacman.move_dir
