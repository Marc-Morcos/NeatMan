block_size = 30
half_block_size = block_size / 2
offset = block_size * 2
pellet_size = 6
power_pellet_size = 12
house_x = 14
house_y = 13
spawn_x = 14
spawn_y = 17
pellet_score = 10
power_pellet_score = 50
ghost_scores = [200, 400, 800, 1600]
# Fruit images from https://static.wikia.nocookie.net/pacman/images/2/25/Fruits_Points.png/revision/latest?cb=20210921001546
fruit_images = ["FruitImgs/cherry.png", "FruitImgs/strawberry.png", "FruitImgs/orange.png", "FruitImgs/apple.png", "FruitImgs/melon.png", "FruitImgs/starship.png", "FruitImgs/bell.png", "FruitImgs/key.png"]
fruit_scores = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
fruit_time = 10
life_points = 10000

#Video settings
MapSizeX = 28
MapSizeY = 31
scaling_factor = 0.7 #factor by which we scale dimensions of game window

#Quick Toggles
neatMode = True #puts the model into a training loop
neatLoadMode = False #Loads an old neat model (CANT HAVE BOTH THIS AND NEATMODE TRUE)
checkpointFolder = "Checkpoints"
modelCheckpoint = "NeatBoi0.pkl"
fastMode = False #No longer human playable, increases speed of game to absolute limits
neatFrameShow = 512 #show every x frames when in fastMode, try to have this be a power of 2
showFPS = False #shows fps, use for testing, prints clutter and slow down program
turnOffGhosts = False
scoreTimeConstraint = 100*60 #dies if doesn't score within this many frames, set to None if you want to turn this of, only works in neatmode
evaluateModelMode = False #runs the selected model for a select number of games and then prints the models statistics 
numberOfTests = 30 #number of games to evaluate on
IdlePenalty = 0#1/60 #if in neatmode, decreases score while sitting idle by this ammount every frame
wrapAround = True #whether camera view screen should wrap around in the x axis
neatLives = 2 #number of lives neatMan has while training in neatmode
backTrackPenalty = 0#2/60 #Applies a penalty for turning around (like full 180) in case your model likes to just spam back and forth
sabotagePenalty = 0#400 #penalty for going towards a non blue, non dead ghost, that is also going towards it (if ur other penalties are too high, pacman tries to kill himself, this fixes that)
sparseMode = False #if true, 50% of only 1 out of 5 pellets spawning

# where we load a whole population to continue training
# set to None to train from scratch
LoadTrainingCheckpointPath = None 
#LoadTrainingCheckpointPath = checkpointFolder + "/NeatBoiPopulation15x15Gen299" 
LoadTrainingCheckpointGenerationNum = 299 #if LoadTrainingCheckpointPath is not None, generations starts at this

neatConfigPath = "neatConfig.text"

#hyperparameters (more hyperparams in config.text)
neatHyperparams = {"NeatNumGenerations":1700, 
                  "NumGenB4MapSwitch":1,
                  "NumGenB4Checkpoint":20,
                  "SecondsB4Checkpoint":3000,
                  "PopulationCheckpointName": checkpointFolder+ "/NeatBoiPopulation15x15Gen",
                  "modelName": "NeatBoi15x15Gen"
                  }

#movement constants
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3