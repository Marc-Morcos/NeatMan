#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
from functools import partial
import neat
from Constants import *

#run a generation of pacmen
def eval_Pacman(genomes, config, gameLoop = None,pacman = None):
    
    for genome_id, genome in genomes:
        pacman.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        gameLoop(fitness = genome.fitness)

    return

#initializes neat stuff
def neatInit(game_loop,pac_man):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        neatConfigPath
    )

    population = neat.Population(config)

    #we want to pass extra stuff into eval_pacman
    newLoop = partial(eval_Pacman,gameLoop=game_loop,pacman=pac_man)

    population.run(newLoop, NeatNumGenerations)
    return population