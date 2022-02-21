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
scaling_factor = 0.7 #factor by which we scale dimensions of game window

pacmanController = humanPlayer #options: dummy, humanPlayer

fastMode = False #No longer human playable, increases speed of game to absolute limits
neatFrameShow = 512 #show every x frames when in fastMode, try to have this be a power of 2
showFPS = False #shows fps, use for testing, prints clutter and slow down program


class Main:
    def __init__(self):
        self.maze_width = 28
        self.maze_height = 31

        self.lives = 2
        self.last_life_score = 0

        self.display_width = self.maze_width * block_size
        self.display_height = self.maze_height * block_size + offset

        self.fps = 60
        if(fastMode): self.fps = 999999999
        self.fps_clock = pygame.time.Clock()
        self.tick_counter = 1
        self.temp_counter = 0

        self.score = 0
        self.collected_pellets = 0
        self.pellets = []
        self.power_pellets = []
        self.num_fruit = 0
        self.running = True

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
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return

    def loop(self):
        if self.game_state == "run":
            # activate inky once 30 coins have been collected
            if self.ghosts["inky"].mode == "house" and self.collected_pellets > 30:
                self.ghosts["inky"].mode = "normal"
            # activate clyde once 1/3 of total coins have been collected
            if self.ghosts["clyde"].mode == "house" and self.collected_pellets > len(self.pellets) / 3:
                self.ghosts["clyde"].mode = "normal"

            self.player.move(self.maze, self.display_width, self.ghosts, self.power_pellets, self.power_pellets, self.fruit)

            if self.player.update_power_up():
                for ghost in self.ghosts.values():
                    if ghost.mode != "dead" and not ghost.blue:
                        ghost.blue = True
                        ghost.blue_timer = 0

            for pellet in self.pellets:
                if pellet.collide(self.player):
                    self.collected_pellets += 1
                    self.score += pellet_score

            for power_pellet in self.power_pellets:
                if power_pellet.collide(self.player):
                    self.score += power_pellet_score
                    self.player.power_up(8 * 60)

            for ghost in self.ghosts.values():
                ghost.move(self.player, self.maze, self.display_width, self.tick_counter, self.ghosts["blinky"].array_coord)
                if ghost.collide(self.player):
                    if ghost.blue and ghost.mode != "dead":
                        ghost.mode = "dead"
                        self.score += ghost_scores[self.player.ghosts_eaten]
                    else:
                        if self.lives > 0:
                            self.game_state = "respawn"
                            self.fruit.here = False
                            self.lives -= 1
                            self.temp_counter = 0
                        else:
                            self.game_state = "lose"

            # Update fruit
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

            self.score += self.fruit.collide(self.player)

            if self.score - self.last_life_score >= life_points:
                self.lives += 1
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
            ghost.draw(surface, self.player, self.tick_counter)

        game_font = pygame.freetype.SysFont("Helvetica.ttf", 40)
        game_font.render_to(surface, (15, 15), "SCORE: " + str(self.score), (255, 255, 255))
        game_font = pygame.freetype.SysFont("Helvetica.ttf", 20)
        game_font.render_to(surface, (400, 15), str(self.lives) + " LIVES", (255, 255, 255))
        game_font.render_to(surface, (600, 15), "FRUIT: ", (255, 255, 255))

        #scaling code from https://stackoverflow.com/questions/43196126/how-do-you-scale-a-design-resolution-to-other-resolutions-with-pygame
        frame = pygame.transform.scale(surface, (self.display_width*scaling_factor, self.display_height*scaling_factor))
        window.blit(frame, frame.get_rect())

    def run(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("NEAT-MAN")
        display = pygame.display.set_mode((self.display_width*scaling_factor, self.display_height*scaling_factor))
        display_surf = pygame.Surface([self.display_width, self.display_height])
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
            self.pellets.append(Pellet(loc[0], loc[1]))

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

        # running game loop
        while self.running:
            if self.game_state in ("run", "respawn"):

                # main game loop
                self.events(self.player)
                self.loop()
                self.draw(display_surf, display)

                # check win condition
                if self.collected_pellets >= len(self.pellets):
                    self.level += 1
                    self.collected_pellets = 0

                    self.player = Pac_Man(spawn_x, spawn_y)

                    # generate all pellets and power pellets
                    self.power_pellets = []
                    for loc in self.maze.power_pellet_locs:
                        self.power_pellets.append(PowerPellet(loc[0], loc[1]))
                    self.pellets = []
                    for loc in self.maze.pellet_locs:
                        self.pellets.append(Pellet(loc[0], loc[1]))

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

                if((not fastMode) or (self.tick_counter%neatFrameShow == 0)): 
                    pygame.display.flip()
                    if(showFPS): print("fps:",self.fps_clock.get_fps()) 
                self.fps_clock.tick(self.fps)
                self.tick_counter += 1

            # end game at win/lose
            elif self.game_state == "win":
                self.running = False
                print("score:",self.score)
            elif self.game_state == "lose":
                self.running = False
                print("score:",self.score)


if __name__ == "__main__":
    main = Main()
    main.run()
