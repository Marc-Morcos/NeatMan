from mazegen.mapgen import mapgen

    #0 = pellet
    #1 = wall
    #2 = ghost door
    #3 = empty space
    #4 seems to be pellet block but is seperate for some reason

#I also edited the mapgen js so we always get 1 tunnel instead of 2
#TODO test if random tunnels crash the game

#creates a converted and cleaned up random map with 28 columns and 31 rows (overwrites mapArray)
#also returns power pellet coordinates
def createMap(mapArray):

    #initial map
    tiles = mapgen.mapgen().tiles.lstrip("_").rstrip("_")

    #convert to readable format
    for row in range(31):
        for col in range(28):
            char = tiles[row*28+col]

            #wall
            if char == '|':
                mapArray[row][col] = 1
            
            #pellet
            elif char == '.' or char == ' ':
                mapArray[row][col] = 0
            
            #empty space
            elif char == '_':
                mapArray[row][col] = 3
            
            #power up
            elif char == 'o':
                #TODO
                mapArray[row][col] = 0

            #ghost door
            elif char == '-':
                mapArray[row][col] = 2
                
            else:
                print("unknown character '", char, "' encountered in mapgenclean")
                mapArray[row][col] = 3
                temp = [(tiles[i:i+28]) for i in range(0, len(tiles), 28)]
                for tempRow in temp:
                    print(tempRow)


    #cleanup
    #shrink ghost area
    for i in range(10,17):
        mapArray[14][i] = 1
        mapArray[15][i] = 1

    #TODO

    #return power pellet coordinates: #TODO
    #return powerUpCoordinates




    #Map example (wrong size)
    #0 = pellet
    #1 = wall
    #2 = ghost door
    #3 = empty space
    #4 seems to be pellet block but is seperate for some reason

            # self.maze_array[0]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            # self.maze_array[1]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            # self.maze_array[2]  = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
            # self.maze_array[3]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            # self.maze_array[4]  = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
            # self.maze_array[5]  = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
            # self.maze_array[6]  = [1, 1, 1, 1, 0, 1, 1, 1, 4, 1, 4, 1, 1, 1, 0, 1, 1, 1, 1]
            # self.maze_array[7]  = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
            # self.maze_array[8]  = [1, 1, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            # self.maze_array[9]  = [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0]
            # self.maze_array[10] = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            # self.maze_array[11] = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
            # self.maze_array[12] = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            # self.maze_array[13] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            # self.maze_array[14] = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
            # self.maze_array[15] = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
            # self.maze_array[16] = [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1]
            # self.maze_array[17] = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
            # self.maze_array[18] = [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
            # self.maze_array[19] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            # self.maze_array[20] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]