import random
from Maze import Maze
from Items import *
from Ghost import Ghost
from Constants import *
from Pac_Man import Pac_Man

#random moves -> no smart
def dummy(pac_man, maze, ghosts, pellets, power_pellets, fruit):
    if(random.randint(0,10) == 0):
        return random.randint(0,4)
    return pac_man.move_dir

#human controlled pacman
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
        print(possible_dirs)
        next = random.sample(possible_dirs, 1)[0]
        print(next)
        return next
    return pac_man.move_dir
