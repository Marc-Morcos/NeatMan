import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from Pac_Man import Pac_Man

def dummy(pacman, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pacman.move_dir

def humanPlayer(pacman, maze, ghosts, pellets, power_pellets, fruit):
    return pacman.humanInput
