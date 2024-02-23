import os
import argparse

IGNORE_TILE = '.'

def read_file(file_path):
    map = []
    solids = []

    with open(file_path) as f:
        for line in f.readlines():
            map.append(list(line.strip()))
            solids.append([c != IGNORE_TILE for c in line.strip()])

    return map, solids


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Tile Map Generator")
    parser.add_argument('--example', help='Example level with tiles correctly places.', type=str, required=True) 
    parser.add_argument('--convert', help='Convert a level given an example level', type=str, required=False)
    parser.add_argument('--output-map', help="Output the map generated from the example to a json file", required=False)
    parser.add_argument('--input-type', help='Whether example level is ascii or image based', choices=['ascii', 'img'], required=True)
    parser.add_argument('--ignore-corners', help='Bitmask operations can ignore corners if two neighboring cardinal directions are also empty.', type=bool, required=False)
    args = parser.parse_args()

    # TODO: handle tile size if image in arg parse

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
