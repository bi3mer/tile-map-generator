import argparse
import json
import os
from typing import List, Tuple

from PIL import Image, ImageChops

from bit_operations import get_bit_mask, get_bit_mask_ignore_corners

TO_CONVERT_TILE = "X"


def get_cmd_args():
    parser = argparse.ArgumentParser("Image Tile Map Decorator")
    parser.add_argument(
        "--tile-size",
        help="Tile size (e.g. 16x16 -> 16)",
        type=int,
    )
    parser.add_argument(
        "--tileset",
        help="Tile set that contains all tiles that are relevant.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--example",
        help="Example level with tiles correctly places.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--convert",
        help="Convert a level given an example level",
        type=str,
        required=False,
        default=None,
    )
    parser.add_argument(
        "--bit-dict",
        help="Output the bitmask dictionary to json dictionary",
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        "--ignore-corners",
        help="Bitmask operations can ignore corners if two neighboring cardinal directions are also empty.",
        action="store_true",
        required=False,
    )

    return parser.parse_args()


def get_image(file_path):
    if not os.path.exists:
        print(f"Image not found: {file_path}")
        exit(-1)

    return Image.open(file_path).convert("RGBA")


def image_to_matrix(image, tilesize):
    matrix = []
    # Get image dimensions and make sure that the tilesize correctly matches
    # the tileset
    W, H = image.size

    assert W % tilesize == 0
    assert H % tilesize == 0

    TW = W // tilesize
    TH = H // tilesize

    # Read image row by row and put the results into a matrix
    for y in range(TH):
        matrix.append([])
        START_Y = y * tilesize
        END_Y = START_Y + tilesize

        for x in range(TW):
            START_X = x * tilesize
            END_X = START_X + tilesize

            matrix[-1].append(image.crop((START_X, START_Y, END_X, END_Y)))

    return matrix


def image_to_tilset(image, tilesize):
    matrix = image_to_matrix(image, tilesize)

    # Read image row by row and put the results into a dictionary
    tileset = {}  # { (x, y): CROPPED_IMAGE }
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            tileset[(x, y)] = matrix[y][x]

    return tileset


def tileset_contains(tileset, img):
    for coord, i in tileset.items():
        diff = ImageChops.difference(i, img)
        if not diff.getbbox():
            return coord  # Image found

    # Image not found
    return None


def image_to_map_and_matrix(image, tileset, tilesize):
    matrix = image_to_matrix(image, tilesize)
    map: List[List[Tuple[int, int] | None]] = []

    for y in range(len(matrix)):
        map.append([])
        for x in range(len(matrix[0])):
            map[-1].append(tileset_contains(tileset, matrix[y][x]))

    return map, matrix


def main():
    args = get_cmd_args()

    # Validate tile size
    tilesize = args.tile_size
    if tilesize <= 0:
        print(f'Error: arg "--tile-size" value too small ({tilesize} <= 0')
        exit(-1)

    # Set correct bitmask
    if args.ignore_corners:
        bitmask_finder = get_bit_mask_ignore_corners
    else:
        bitmask_finder = get_bit_mask

    # get the tileset
    tileset = image_to_tilset(get_image(args.tileset), tilesize)

    # convert example image of a map to a matrix of booleans
    map, matrix = image_to_map_and_matrix(get_image(args.example), tileset, tilesize)

    for row in map:
        print("".join("," if e == None else "X" for e in row))

    # if args.convert:
    #     convert_level(args.convert, bitmask_finder, bitmaskToTile)
    #
    # if args.bit_dict:
    #     output_bitmask_dictionary(args.bit_dict, bitmaskToTile)


if __name__ == "__main__":
    main()


def read_file_for_conversion(file_path):
    map = []
    to_convert = []

    with open(file_path) as f:
        for line in f.readlines():
            map.append(list(line.strip()))
            to_convert.append([c == TO_CONVERT_TILE for c in line.strip()])

    return map, to_convert


def read_example_level(example_level, bitmask_finder):
    if not os.path.exists(example_level):
        print(f"Could not read the example level: {example_level}")
        exit(-1)

    map, solids = read_file(example_level)
    bitmaskToTile = {}

    for y in range(len(map)):
        for x in range(len(map[0])):
            if not solids[y][x]:
                continue  # we only care about relevant tiles

            bitmask = bitmask_finder(solids, x, y)
            char = map[y][x]

            if bitmask in bitmaskToTile and char != bitmaskToTile[bitmask]:
                print(
                    f"Error! Matching bitmasks found for {char} and {bitmaskToTile[char]}"
                )
                exit(-1)
            else:
                bitmaskToTile[bitmask] = char

    return bitmaskToTile


def convert_level(level, bitmask_finder, bitmaskToTile):
    if not os.path.exists(level):
        print(f"Could not read level to convert: {level}")
        exit(-1)

    convert_map, convert_solids = read_file(level)

    for y in range(len(convert_map)):
        for x in range(len(convert_map[0])):
            if not convert_solids[y][x]:
                continue

            bitmask = bitmask_finder(convert_solids, x, y)
            if bitmask in bitmaskToTile:
                convert_map[y][x] = bitmaskToTile[bitmask]

    print("\n".join("".join(line) for line in convert_map))


def output_bitmask_dictionary(output_file, bitmaskToTile):
    with open(output_file, "w") as f:
        json.dump(bitmaskToTile, f, indent=2)
