tiles = [(tiles[i:i+31]) for i in range(0, len(tiles), 31)]
for array in tiles:
    print(array)