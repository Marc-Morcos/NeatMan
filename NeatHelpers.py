#our neat implementation is based on this tutorial https://www.youtube.com/watch?v=CKFCIzPSBjE&ab_channel=CodeBucket
# def eval_Pacman:
#     return score or smthing idk

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