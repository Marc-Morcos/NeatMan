#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
#and this documentation https://neat-python.readthedocs.io/en/latest/xor_example.html
from functools import partial
import neat
from Constants import *

#run a generation of pacmen
def eval_Pacman(genomes, config, main = None):
    
    maxFitness = 0
    maxFitnessId = -1
    for genome_id, genome in genomes:
        main.player.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = main.game_loop()
        main.reset(hard = True, newMap = False) #reset for next pac in generation
        if genome.fitness > maxFitness:
            maxFitness = genome.fitness
            maxFitnessId = genome_id

    
    #generate a new map and reset for next generation
    main.reset(hard = True, newMap = ((main.current_generation % neatHyperparams["NumGenB4MapSwitch"]) == 0))
    #print("Current Generation:", main.current_generation, ", Max Gen Fitness:", maxFitness, ", Max Gen Fitness ID:", maxFitnessId)
    main.current_generation += 1

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

    population.run(newLoop, neatHyperparams["NeatNumGenerations"])
    return population