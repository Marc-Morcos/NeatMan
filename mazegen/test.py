from mapgen import mapgen

map = mapgen.mapgen()

tiles = map.tiles.lstrip("_").rstrip("_")
tiles = [(tiles[i:i+28]) for i in range(0, len(tiles), 28)]
for array in tiles:
    print(array)