#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
#and this repo https://github.com/codewmax/neat-chrome-dinosaur/blob/master/main.py
#and this documentation https://neat-python.readthedocs.io/en/latest/xor_example.html
from functools import partial
import neat
from Constants import *
import os
import pickle

#saves a specific model
def saveModel(model,generation,config):
    fileName = os.path.join(checkpointFolder,neatHyperparams["modelName"]+str(generation)+".pkl")
    outfile = open(fileName,'wb')
    pickle.dump(model,outfile)
    outfile.close()

    fileName = os.path.join(checkpointFolder,neatHyperparams["modelName"]+str(generation)+".pklconfig")
    outfile = open(fileName,'wb')
    pickle.dump(config,outfile)
    outfile.close()

#loads a specific model
def loadModel(name):
    fileName = os.path.join(checkpointFolder,name)
    infile = open(fileName,'rb')
    net = pickle.load(infile)
    infile.close()

    fileName = os.path.join(checkpointFolder,name+"config")
    infile = open(fileName,'rb')
    config = pickle.load(infile)
    infile.close()

    net = neat.nn.FeedForwardNetwork.create(net, config)
    return net


#run a generation of pacmen
def eval_Pacman(genomes, config, main = None):

    maxScore = 0
    maxScoreGenes = -1
    for genome_id, genome in genomes:
        main.player.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = main.game_loop()
        main.reset(hard = True, newMap = False) #reset for next pac in generation
        if genome.fitness>maxScore:
            maxScore=genome.fitness
            maxScoreGenes = genome
    
    #save the best model
    if (main.current_generation % neatHyperparams["NumGenB4Checkpoint"] == 0):
        saveModel(maxScoreGenes,main.current_generation,config)

    
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

    if(LoadTrainingCheckpointPath == None):
        population = neat.Population(config)
    else:
        population = neat.Checkpointer.restore_checkpoint(LoadTrainingCheckpointPath)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(neatHyperparams["NumGenB4Checkpoint"], None, neatHyperparams["PopulationCheckpointName"]))

    #we want to pass extra stuff into eval_pacman
    newLoop = partial(eval_Pacman,main=main)

    winner = population.run(newLoop, neatHyperparams["NeatNumGenerations"])

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    #save winner
    saveModel(model+"WINNER",neatHyperparams["NeatNumGenerations"],config)

    return population