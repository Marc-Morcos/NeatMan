#this project is built on this repo https://github.com/moritree/PY-MAN

import pygame
import pygame.freetype
from Maze import Maze
from Pac_Man import Pac_Man
from Items import *
from Ghost import Ghost
from Constants import *
from pygame.locals import *
from movementAlgos import *
from NeatHelpers import *
import neat
import random

pacmanController = humanPlayer #  #options: dummy, humanPlayer, neat, avoid_ghost_and_wall_dummy, pathFind_to_target

if(neatMode): 
    pacmanController = modelNeat

if(neatLoadMode):
    pacmanController = modelNeat

class Main:
    def __init__(self):
        self.maze_width = MapSizeX
        self.maze_height = MapSizeY
        self.current_generation = 1
        if LoadTrainingCheckpointPath != None:
            self.current_generation = LoadTrainingCheckpointGenerationNum

        self.last_life_score = 0

        self.display_width = self.maze_width * block_size
        self.display_height = self.maze_height * block_size + offset

        self.fps = 60
        if(fastMode): self.fps = 99999999
        self.fps_clock = pygame.time.Clock()
        self.tick_counter = 1
        self.temp_counter = 0

        self.score = 0
        self.lastFrameScore = 0
        self.framesUntilOutOfTime = scoreTimeConstraint

        self.collected_pellets = 0
        self.pellets = []
        self.power_pellets = []
        self.num_fruit = 0
        self.running = True
        self.coinFlip = (random.choice([0,1]) == 1)
        self.manuallySave = False #keep this false

        self.game_state = "run"
        self.level = 0

    def events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.humanInput = UP
                if event.key == pygame.K_DOWN:
                    player.humanInput = DOWN
                if event.key == pygame.K_LEFT:
                    player.humanInput = LEFT
                if event.key == pygame.K_RIGHT:
                    player.humanInput = RIGHT
                if event.key == pygame.K_COMMA:
                    printMaze(self.maze.maze_array)
                    print("pac_man_x: {} pac_man_y: {}".format(self.player.x, self.player.y))
                if event.key == pygame.K_EQUALS and neatMode:
                    self.player.lives = -1
                    self.game_state = "lose"
                    self.manuallySave = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return

    def loop(self):
        #kill score
        if(neatMode and killScore!=None and self.score >= killScore):
            self.player.lives = -1
            self.game_state = "lose"

        #die if you don't score fast enough
        if scoreTimeConstraint != None and (neatMode):
            if self.lastFrameScore==self.score:
                self.framesUntilOutOfTime-=1
                if self.framesUntilOutOfTime <=0:
                     self.framesUntilOutOfTime = scoreTimeConstraint
                     if self.player.lives > 0:
                            self.player.target = 0
                            self.game_state = "respawn"
                            self.fruit.here = False
                            self.player.lives -= 1
                            self.temp_counter = 0
                     else:
                            self.game_state = "lose"
            else:
                self.framesUntilOutOfTime = scoreTimeConstraint
        
        self.lastFrameScore =self.score 
        self.player.pelletRatio =  self.collected_pellets/len(self.pellets)

        if self.game_state == "run":
            # activate inky once 30 coins have been collected
            if self.ghosts["inky"].mode == "house" and self.collected_pellets > 30:
                self.ghosts["inky"].mode = "normal"
            # activate clyde once 1/3 of total coins have been collected
            if self.ghosts["clyde"].mode == "house" and self.collected_pellets > len(self.pellets) / 3:
                self.ghosts["clyde"].mode = "normal"

            #this only decreases score in neatmode (look at the move function)
            scoreB4 = self.score
            self.score -= self.player.move(maze = self.maze, display_width = self.display_width, ghosts = self.ghosts, power_pellets = self.power_pellets, pellets = self.pellets, fruit = self.fruit)
            if(self.lastFrameScore == scoreB4):
                self.lastFrameScore = self.score #simulates the score not increasing

            if self.player.update_power_up():
                for ghost in self.ghosts.values():
                    if ghost.mode != "dead" and not ghost.blue:
                        ghost.blue = True
                        ghost.blue_timer = 0

            for pellet in self.pellets:
                if pellet.collide(self.player):
                    self.collected_pellets += 1
                    self.score += pellet_score*(1+self.collected_pellets*clearMapBonus/251)

            for power_pellet in self.power_pellets:
                if power_pellet.collide(self.player) and (not disablePowerPellets or not neatMode):
                    self.score += power_pellet_score*(1+self.collected_pellets*clearMapBonus/251)
                    self.player.power_up(8 * 60)

            for ghost in self.ghosts.values():
                ghost.move(self.player, self.maze, self.display_width, self.tick_counter, self.ghosts["blinky"].array_coord)
                if ghost.collide(self.player):
                    if ghost.blue and ghost.mode != "dead":
                        ghost.mode = "dead"
                        self.score += ghost_scores[self.player.ghosts_eaten]*(1+self.collected_pellets*clearMapBonus/251)
                        self.player.ghosts_eaten +=1
                    else:
                        if self.player.lives > 0:
                            self.player.target = 0
                            self.game_state = "respawn"
                            self.fruit.here = False
                            self.player.lives -= 1
                            self.temp_counter = 0
                        else:
                            self.game_state = "lose"

            # Update fruitdisplayWidth
            self.fruit.update()

            # Give fruit
            if self.num_fruit == 0 and self.collected_pellets >= len(self.pellets) / 3:
                self.fruit.time = fruit_time * 60
                self.fruit.here = True
                self.num_fruit += 1
            elif self.num_fruit == 1 and self.collected_pellets >= len(self.pellets) * 2/3:
                self.fruit.time = fruit_time * 60
                self.fruit.here = True
                self.num_fruit += 1

            self.score += self.fruit.collide(self.player)*(1+self.collected_pellets*clearMapBonus/251)

            if self.score - self.last_life_score >= life_points:
                self.player.lives += 1
                self.last_life_score += life_points

    def draw(self, surface, window):
        if(fastMode and (self.tick_counter%neatFrameShow != 0)):
            if self.game_state == "respawn":
                if self.temp_counter < 36:
                    self.temp_counter += 1
                else:
                    self.game_state = "run"
                    self.player.x = spawn_x * block_size + block_size / 2
                    self.player.y = spawn_y * block_size + block_size / 2
                    for ghost in self.ghosts.values():
                        if(ghost.mode != "house"):
                            ghost.x = house_x* block_size + block_size / 2
                            ghost.y = house_y* block_size + block_size / 2
            return

        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.display_width, self.display_height))

        self.maze.draw(surface)

        self.display_fruit.draw(surface)
        self.fruit.draw(surface)

        for power_pellet in self.power_pellets:
            power_pellet.draw(surface)
        for pellet in self.pellets:
            pellet.draw(surface)

        if self.game_state == "run":
            self.player.draw_while_running(surface, self.display_width, self.maze, self.tick_counter)
        elif self.game_state == "respawn":
            if self.temp_counter < 36:
                self.player.draw_wedge_pacman(surface, 0 + 10 * self.temp_counter)
                self.temp_counter += 1
            else:
                self.game_state = "run"
                self.player.x = spawn_x * block_size + block_size / 2
                self.player.y = spawn_y * block_size + block_size / 2
                self.player.draw_while_running(surface, self.display_width, self.maze, self.tick_counter)
                for ghost in self.ghosts.values():
                            if(ghost.mode != "house"):
                                ghost.x = house_x* block_size + block_size / 2
                                ghost.y = house_y* block_size + block_size / 2

        for ghost in self.ghosts.values():
            ghost.draw(surface, self.player, self.tick_counter)

        game_font = pygame.freetype.SysFont("Helvetica.ttf", 40)
        game_font.render_to(surface, (15, 15), "SCORE: " + str(int(self.score)), (255, 255, 255))
        game_font = pygame.freetype.SysFont("Helvetica.ttf", 20)
        game_font.render_to(surface, (400, 15), str(self.player.lives) + " LIVES", (255, 255, 255))
        game_font.render_to(surface, (600, 15), "FRUIT: ", (255, 255, 255))

        #scaling code from https://stackoverflow.com/questions/43196126/how-do-you-scale-a-design-resolution-to-other-resolutions-with-pygame
        frame = pygame.transform.scale(surface, (self.display_width*scaling_factor, self.display_height*scaling_factor))
        window.blit(frame, frame.get_rect())

    #resets the game
    #if hard is false, we are just moving to a new level
    #if hard is true, its a true reset
    def reset(self, hard = False, newMap = False,coinFlip = False):
        net = self.player.net
        newlives = self.player.lives
        if(coinFlip): self.coinFlip = (random.choice([0,1]) == 1)
        #hard reset  
        if(hard):
            newlives = 2
            if(neatMode): newlives = neatLives
            self.last_life_score = 0
            self.score = 0
            self.level = 0         
        #soft reset
        else:
            self.level += 1

        self.framesUntilOutOfTime = scoreTimeConstraint
        
        #make a new map
        if newMap:
            self.maze = Maze(self.maze_width, self.maze_height) #regen maze

        self.collected_pellets = 0
        self.temp_counter = 0

        self.player = Pac_Man(spawn_x, spawn_y,pacmanController)
        self.player.net = net
        self.player.lives = newlives

        # generate all pellets and power pellets
        self.power_pellets = []
        for loc in self.maze.power_pellet_locs:
            self.power_pellets.append(PowerPellet(loc[0], loc[1]))
        self.pellets = []
        for loc in self.maze.pellet_locs:
            self.pellets.append(Pellet(loc[0], loc[1],(neatMode and sparseMode and self.coinFlip)))

        self.ghosts = {}

        # spawn ghosts
        self.ghosts["blinky"] = Ghost(house_x, house_y-2, (255, 80, 80), [house_x+7, house_y-7], "shadow")
        self.ghosts["pinky"] = Ghost(house_x-1, house_y, (255, 100, 150), [house_x-7, house_y-7], "speedy")
        self.ghosts["inky"] = Ghost(house_x, house_y, (100, 255, 255), [house_x+7, house_y+9], "bashful")
        self.ghosts["clyde"] = Ghost(house_x+1, house_y, (255, 200, 000), [house_x-7, house_y+9], "pokey")

        self.ghosts["blinky"].mode = "normal"
        self.ghosts["pinky"].mode = "normal"

        # spawn fruit
        self.num_fruit = 0
        self.display_fruit = Fruit(23, -2, fruit_scores[self.level % 8], pygame.image.load(fruit_images[self.level % 8]), True)
        self.fruit = Fruit(spawn_x, spawn_y, fruit_scores[self.level % 8], pygame.image.load(fruit_images[self.level % 8]), False)

    #main loop of the game
    def game_loop(self):
        while self.running:
            if self.game_state in ("run", "respawn"):
                # main game loop
                self.events(self.player)
                self.loop()
                self.draw(self.display_surf, self.display)

                # check win condition
                if self.collected_pellets >= len(self.pellets):
                    self.game_state = "win"
                    
                if((not fastMode) or (self.tick_counter%neatFrameShow == 0)): 
                    pygame.display.flip()
                    if(showFPS): print("fps:",self.fps_clock.get_fps()) 
                self.fps_clock.tick(self.fps)
                self.tick_counter += 1

            # What to do when we win/lose
            elif self.game_state == "win":
                self.reset()
                print("won level, moving on, score:",self.score)
                self.game_state = "run"
            elif self.game_state == "lose":
                self.running = False
                if(neatMode or evaluateModelMode): 
                    self.running = True
                    self.game_state = "run"
                    return self.score #update fitness
                print("score:",self.score)

    def run(self):
        # initialize
        random.seed()
        pygame.init()
        pygame.display.set_caption(neatHyperparams["modelName"])
        self.display = pygame.display.set_mode((int(self.display_width*scaling_factor), int(self.display_height*scaling_factor)))
        self.display_surf = pygame.Surface([self.display_width, self.display_height])
        pygame.font.init()

        # spawn maze and player
        self.maze = Maze(self.maze_width, self.maze_height)
        self.player = Pac_Man(spawn_x, spawn_y, pacmanController)

        # generate all pellets and power pellets
        self.power_pellets = []
        for loc in self.maze.power_pellet_locs:
            self.power_pellets.append(PowerPellet(loc[0], loc[1]))
        self.pellets = []
        for loc in self.maze.pellet_locs:
            self.pellets.append(Pellet(loc[0], loc[1],(neatMode and sparseMode and self.coinFlip)))

        self.ghosts = {}

        # spawn ghosts
        self.ghosts["blinky"] = Ghost(house_x, house_y-2, (255, 80, 80), [house_x+7, house_y-7], "shadow")
        self.ghosts["pinky"] = Ghost(house_x-1, house_y, (255, 100, 150), [house_x-7, house_y-7], "speedy")
        self.ghosts["inky"] = Ghost(house_x, house_y, (100, 255, 255), [house_x+7, house_y+9], "bashful")
        self.ghosts["clyde"] = Ghost(house_x+1, house_y, (255, 200, 000), [house_x-7, house_y+9], "pokey")

        self.ghosts["blinky"].mode = "normal"
        self.ghosts["pinky"].mode = "normal"

        # spawn fruit
        self.display_fruit = Fruit(23, -2, fruit_scores[self.level % 8], pygame.image.load(fruit_images[self.level % 8]).convert(), True)
        self.fruit = Fruit(spawn_x, spawn_y, fruit_scores[self.level % 8], pygame.image.load(fruit_images[self.level % 8]).convert(), False)

        #the gameloop is elsewhere for neat
        if (not neatMode and not evaluateModelMode): self.game_loop()

        #initialize neat stuff
        if neatMode: neatInit(self) 

        #initialize eval mode
        if evaluateModelMode: evaluateModelInit(self) 


if __name__ == "__main__":
    main = Main()
    main.run()
