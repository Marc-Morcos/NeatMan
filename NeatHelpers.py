#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
from functools import partial
import neat
from Constants import *

#run a generation of pacmen
def eval_Pacman(genomes, config, main = None):
    
    for genome_id, genome in genomes:
        main.player.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = main.game_loop()
        main.reset(hard = True, newMap = False) #reset for next pac in generation
        print("fitness:",genome.fitness)

    #generate a new map and reset for next generation
    main.reset(hard = True, newMap = True)

    return

#initializes neat stuff
def neatInit(main):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        neatConfigPath
    )

    population = neat.Population(config)

    #we want to pass extra stuff into eval_pacman
    newLoop = partial(eval_Pacman,main=main)

    population.run(newLoop, NeatNumGenerations)
    return population