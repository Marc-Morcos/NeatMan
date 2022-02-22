#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
import neat
from Constants import *

def eval_Pacman(genomes, config):
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
    

    return

#initializes neat stuff
def neatInit():
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        neatConfigPath
    )

    population = neat.Population(config)
    population.run(eval_Pacman, NeatNumGenerations)
    return population