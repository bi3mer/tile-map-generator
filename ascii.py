import argparse
import json
import os
from bit_operations import large_bit_mask

from common_functions import (
    bit_mask_to_tile_from_example_ascii,
    convert_level,
    get_bit_mask_lambda,
    read_text_level,
)


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


def read_example_level(example_level, bitmask_finder):
    map, solids = read_text_level(example_level)
    return bit_mask_to_tile_from_example_ascii(map, solids, bitmask_finder)


def main():
    args = get_cmd_args()

    bitmask_finder = get_bit_mask_lambda(args.ignore_corners)
    bitmaskToTile = read_example_level(args.example, bitmask_finder)

    if args.convert:
        level = args.convert
        map_to_convert, mask = read_text_level(level)
        converted_map = convert_level(
            map_to_convert,
            mask,
            bitmaskToTile,
            bitmask_finder,
            fuzzy_match_on_fail=True,
        )

        print("\n".join("".join(line) for line in converted_map))

    if args.bit_dict:
        with open(args.bit_dict, "w") as f:
            json.dump(bitmaskToTile, f, indent=2)


if __name__ == "__main__":
    main()
