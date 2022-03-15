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
ghost_scores = [200, 400, 800, 1600,200, 400, 800, 1600,200, 400, 800, 1600,200, 400, 800, 1600]
# Fruit images from https://static.wikia.nocookie.net/pacman/images/2/25/Fruits_Points.png/revision/latest?cb=20210921001546
fruit_images = ["FruitImgs/cherry.png", "FruitImgs/strawberry.png", "FruitImgs/orange.png", "FruitImgs/apple.png", "FruitImgs/melon.png", "FruitImgs/starship.png", "FruitImgs/bell.png", "FruitImgs/key.png"]
fruit_scores = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
fruit_time = 10
life_points = 10000

#Video settings
MapSizeX = 28
MapSizeY = 31
scaling_factor = 0.7 #factor by which we scale dimensions of game window

#eval
evaluateModelMode = False #runs the selected model for a select number of games and then prints the models statistics 
numberOfTests = 30 #number of games to evaluate on


#Quick Toggles
neatMode = True #puts the model into a training loop
neatLoadMode = False #Loads an old neat model (CANT HAVE BOTH THIS AND NEATMODE TRUE)
checkpointFolder = "Checkpoints" 
modelCheckpoint = "Intuitor5x5Gen.pkl" #30 might be good, 50, 280 may be amazing, 270, 290 might be amazing, 320 might be amazing
fastMode = False #No longer human playable, increases speed of game to absolute limits
neatFrameShow = 60*2 #show every x frames when in fastMode, try to have this be a power of 2
showFPS = False #shows fps, use for testing, prints clutter and slow down program
turnOffGhosts = False
scoreTimeConstraint = 700*60 #dies if doesn't score within this many frames, set to None if you want to turn this of, only works in neatmode
IdlePenalty = 2/60 #if in neatmode, decreases score while sitting idle by this ammount every frame
wrapAroundX = True #whether camera view screen should wrap around in the x axis
wrapAroundY = False #whether camera view screen should wrap around in the y axis
neatLives = 0 #number of lives neatMan has while training in neatmode
backTrackPenalty = 0#2/60 #Applies a penalty for turning around (like full 180) in case your model likes to just spam back and forth
sparseMode = False #if true, 50% of only 1 out of 5 pellets spawning
rotateCamera = True #rotates the camera so that the 'top' of the camera is the direction pacman is facing 
wallBonkPenalty = 0 #1/60 #penalize model from trying to walk into walls
kamikazePenalty = 15 #15 #penalize ghost for running into ghost that is also going towards it (the model should litterally never do this) 
notDumbReward = 0#10/60 #reward applied when a nonegative (according to cammera) move is picked (lookdir*movedir), multiplied by (the value on camera++0.2)
oneOutput = False #turn this on if you want to use the 1 output scheme
wacky2Output = True #a weird 2 output mode
antiRacetrack = False #add walls to prevent spinning around ghost house
clearMapBonus = 0 #5 everything goes up in value as fewer pellets are left on the field

# where we load a whole population to continue training
# set to None to train from scratch
LoadTrainingCheckpointPath = None 
#LoadTrainingCheckpointPath = checkpointFolder + "/Intuitor5x5PopulationGen9" 
LoadTrainingCheckpointGenerationNum = 9 #if LoadTrainingCheckpointPath is not None, generations starts at this

neatConfigPath = "neatConfig.text"

#hyperparameters (more hyperparams in config.text)
neatHyperparams = {"NeatNumGenerations":99999999, 
                  "NumGenB4MapSwitch":5,
                  "NumGenB4Checkpoint":10,
                  "SecondsB4Checkpoint":3000,
                  "PopulationCheckpointName": checkpointFolder+ "/Intuitor5x5PopulationGen",
                  "modelName": "Intuitor5x5Gen"
                  }

#movement constants
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3









#Don't touch
if(not neatMode):
    clearMapBonus = 0
if(neatMode):
    evaluateModelMode = False
    neatLoadMode = False
    fastMode = True
