import argparse
import json
import os

from bit_operations import get_bit_mask, get_bit_mask_ignore_corners

IGNORE_TILE = "."


def get_cmd_args():
    parser = argparse.ArgumentParser("ASCII Tile Map Decorator")
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


def read_file(file_path):
    map = []
    solids = []

    with open(file_path) as f:
        for line in f.readlines():
            map.append(list(line.strip()))
            solids.append([c != IGNORE_TILE for c in line.strip()])

    return map, solids


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


def main():
    args = get_cmd_args()

    if args.ignore_corners:
        bitmask_finder = get_bit_mask_ignore_corners
    else:
        bitmask_finder = get_bit_mask

    bitmaskToTile = read_example_level(args.example, bitmask_finder)

    if args.convert:
        convert_level(args.convert, bitmask_finder, bitmaskToTile)

    if args.bit_dict:
        output_bitmask_dictionary(args.bit_dict, bitmaskToTile)


if __name__ == "__main__":
    main()
