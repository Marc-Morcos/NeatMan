#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
#and this documentation https://neat-python.readthedocs.io/en/latest/xor_example.html
from functools import partial
import neat
from Constants import *

#run a generation of pacmen
def eval_Pacman(genomes, config, main = None):
    
    for genome_id, genome in genomes:
        main.player.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = main.game_loop()
        main.reset(hard = True, newMap = False) #reset for next pac in generation

    
    #generate a new map and reset for next generation
    main.reset(hard = True, newMap = ((main.current_generation % neatHyperparams["NumGenB4MapSwitch"]) == 0))
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

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(neatHyperparams["NumGenB4Checkpoint"], None, neatHyperparams["ModelName"]))

    #we want to pass extra stuff into eval_pacman
    newLoop = partial(eval_Pacman,main=main)

    winner = population.run(newLoop, neatHyperparams["NeatNumGenerations"])

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    return population