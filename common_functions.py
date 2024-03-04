from bit_operations import hamming_distance, get_bit_mask, get_bit_mask_ignore_corners

import os

IGNORE_TILE = "."


def read_text_level(file_path):
    if not os.path.exists(file_path):
        print(f"Could not read the example level: {file_path}")
        exit(-1)

    map = []
    mask = []

    with open(file_path) as f:
        for line in f.readlines():
            map.append(list(line.strip()))
            mask.append([c != IGNORE_TILE for c in line.strip()])

    return map, mask


def get_bit_mask_lambda(ignore_corners):
    if ignore_corners:
        return get_bit_mask_ignore_corners

    return get_bit_mask


# - map: is the set of characters for ascii or tile coords for images as a matrix.
# - mask: matches the matrix of map, except it is true or false for whether it is
#   relevant to the bitmask function
# - bitmask_finder: see bit_operations, it's one of the two functions
def bit_mask_to_tile_from_example_ascii(map, mask, bitmask_finder):
    H = len(map)
    W = len(map[0])
    bitmaskToTile = {}

    for y in range(H):
        for x in range(W):
            if not mask[y][x]:
                continue  # we only care about relevant tiles

            bitmask = bitmask_finder(mask, x, y)
            char = map[y][x]

            if bitmask in bitmaskToTile and char != bitmaskToTile[bitmask]:
                print(
                    f"Error! Matching bitmasks for {char} and {bitmaskToTile[bitmask]} at coordinate ({x}, {y})."
                )

                for _y in range(y - 2, y + 3):
                    _y_condition = y >= 0 and y < H
                    row = ""
                    for _x in range(x - 2, x + 3):
                        if _x == x and _y == y:
                            row += "*"
                        else:
                            row += str(
                                int(
                                    mask[_y][_x]
                                    if _y_condition and _x >= 0 and _x < W
                                    else True
                                )
                            )

                    print(row)

                exit(-1)
            else:
                bitmaskToTile[bitmask] = char

    return bitmaskToTile


def fuzzy_match(bitmask_to_tile, mask, bitmask):
    best_sim = 10000
    best_res = []
    for _mask in bitmask_to_tile.keys():
        sim = hamming_distance(bitmask, _mask, 8)
        if sim < best_sim:
            best_sim = sim
            best_res = [_mask]
        elif sim == best_sim:
            best_res.append(_mask)

    while len(best_res) > 1:
        best_res = [best_res[-1]]

    return best_res[0]


def convert_level(
    map, mask, bitmask_to_tile, bitmask_finder, fuzzy_match_on_fail=False
):
    # copy the map to convert it
    map_to_convert = [r[:] for r in map]

    # run bitmask for all relevant tiles
    for y in range(len(map_to_convert)):
        for x in range(len(map_to_convert[0])):
            if not mask[y][x]:
                continue

            bitmask = bitmask_finder(mask, x, y)
            if bitmask in bitmask_to_tile:
                map_to_convert[y][x] = bitmask_to_tile[bitmask]
            elif fuzzy_match_on_fail:
                map_to_convert[y][x] = bitmask_to_tile[
                    fuzzy_match(bitmask_to_tile, mask, bitmask)
                ]

    # map is now converted
    return map_to_convert
