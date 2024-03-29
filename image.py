import argparse
import json
import os
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageChops

from bit_operations import get_bit_mask, get_bit_mask_ignore_corners, large_bit_mask
from common_functions import (
    bit_mask_to_tile_from_example_ascii,
    convert_level,
    get_bit_mask_lambda,
    read_text_level,
)

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
        END_Y = START_Y + tilesize - 1

        for x in range(TW):
            START_X = x * tilesize
            END_X = START_X + tilesize - 1

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
    np_img = np.asarray(img)
    for coord, tile in tileset.items():
        # for some reason pyright thinks that this is an error.
        if np.sum(np_img - np.asarray(tile)) == 0:  # type: ignore
            return coord  # Image found

    # Image not found
    return None


def read_level_from_image(image, tileset, tilesize):
    matrix = image_to_matrix(image, tilesize)
    coordinates: List[List[Tuple[int, int] | None]] = []
    mask: List[List[bool]] = []

    for y in range(len(matrix)):
        coordinates.append([])
        mask.append([])
        for x in range(len(matrix[0])):
            coordinates[-1].append(tileset_contains(tileset, matrix[y][x]))
            mask[-1].append(coordinates[-1][-1] is not None)

    return mask, matrix, coordinates


def main():
    args = get_cmd_args()

    # Validate tile size
    tilesize = args.tile_size
    if tilesize <= 0:
        print(f'Error: arg "--tile-size" value too small ({tilesize} <= 0')
        exit(-1)

    # Set correct bitmask
    # bitmask_finder = get_bit_mask_lambda(args.ignore_corners)
    bitmask_finder = large_bit_mask

    # get the tileset and use it to load in the example map
    tileset = image_to_tilset(get_image(args.tileset), tilesize)
    mask, _map, coordinates = read_level_from_image(
        get_image(args.example), tileset, tilesize
    )

    # use sample to get a bitmask to tile dictinoary
    bitmaskToTile = bit_mask_to_tile_from_example_ascii(
        coordinates, mask, bitmask_finder
    )

    if args.convert:
        level = args.convert

        c_map, c_mask = read_text_level(level)

        converted_map = convert_level(c_map, c_mask, bitmaskToTile, bitmask_finder)
        for r in converted_map:
            print(r)

    if args.bit_dict:
        with open(args.bit_dict, "w") as f:
            json.dump(bitmaskToTile, f, indent=2)


if __name__ == "__main__":
    main()
