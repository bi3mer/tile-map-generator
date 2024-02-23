import os

IGNORE_TILE = '.'

# Function assumes that top annd bottom rows are not relevant. Same for 
# left and right columns. 
# 1 2 3 
# 4 * 5 
# 6 7 8
def get_bit_mask(map, x, y):
    res = 0  
    res |= (map[y - 1][x - 1]) 
    res |= (map[y- 1][x] << 1) 
    res |= (map[y-1][x+1] << 2) 
    res |= (map[y][x-1] << 3) 
    res |= (map[y][x+1] << 4) 
    res |= (map[y+1][x-1] << 5) 
    res |= (map[y+1][x] << 6) 
    res |= (map[y+1][x+1] << 7)

    return res

# Function assumes that top annd bottom rows are not relevant. Same for 
# left and right columns. 
# 1 2 3 
# 4 * 5 
# 6 7 8
def get_bit_mask_ignore_corners(map, x, y):
    NW = map[y-1][x-1]
    N = map[y-1][x]
    NE = map[y-1][x+1]
    W = map[y][x-1]
    E = map[y][x+1]
    SW = map[y+1][x-1]
    S = map[y+1][x]
    SE = map[y+1][x+1]

    if not (N and W):
        NW = False
    if not (N and E):
        NE = False
    if not (S and W):
        SW = False
    if not (S and E):
        SE = False


    res = 0  
    res |= (NW) 
    res |= (N << 1) 
    res |= (NE << 2) 
    res |= (W << 3) 
    res |= (E << 4) 
    res |= (SW << 5) 
    res |= (S << 6) 
    res |= (SE << 7)

    return res

def read_file(file_path):
    map = []
    solids = []

    with open(file_path) as f:
        for line in f.readlines():
            map.append(list(line.strip()))
            solids.append([c != IGNORE_TILE for c in line.strip()])

    return map, solids

example_level = 'example/ascii/example-lvl.txt'
convert_level = 'example/ascii/input.txt'

if not os.path.exists(example_level):
    print(f'Could not read the example level: {example_level}')

if not os.path.exists(convert_level):
    print(f'Could not read level to convert: {convert_level}')


map, solids = read_file(example_level)
bitmaskToTile = {}

for y in range(len(map)):
    for x in range(len(map[0])):
        if not solids[y][x]:
            continue # we only care about relevant tiles

        bitmask = get_bit_mask_ignore_corners(solids, x, y)
        char = map[y][x]

        if bitmask in bitmaskToTile and char != bitmaskToTile[bitmask]:
            print(f'Error! Matching bitmasks found for {char} and {bitmaskToTile[char]}')
            exit(-1)
        else:
            bitmaskToTile[bitmask] = char

convert_map, convert_solids = read_file(convert_level)

for y in range(len(convert_map)):
    for x in range(len(convert_map[0])):
        if not convert_solids[y][x]:
            continue

        bitmask = get_bit_mask_ignore_corners(convert_solids, x, y)
        convert_map[y][x] = bitmaskToTile[bitmask]


print('\n'.join(''.join(line) for line in convert_map))
