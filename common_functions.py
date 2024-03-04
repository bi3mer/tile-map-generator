from bit_operations import get_bit_mask, get_bit_mask_ignore_corners


def get_bit_mask_lambda(ignore_corners):
    if ignore_corners:
        return get_bit_mask_ignore_corners

    return get_bit_mask


# - map: is the set of characters for ascii or tile coords for images as a matrix.
# - mask: matches the matrix of map, except it is true or false for whether it is
#   relevant to the bitmask function
# - bitmask_finder: see bit_operations, it's one of the two functions
def bit_mask_to_tile_from_example_ascii(map, mask, bitmask_finder):
    bitmaskToTile = {}

    for y in range(len(map)):
        for x in range(len(map[0])):
            if not mask[y][x]:
                continue  # we only care about relevant tiles

            bitmask = bitmask_finder(mask, x, y)
            char = map[y][x]

            if bitmask in bitmaskToTile and char != bitmaskToTile[bitmask]:
                print(
                    f"Error! Matching bitmasks found for {char} and {bitmaskToTile[char]}"
                )
                exit(-1)
            else:
                bitmaskToTile[bitmask] = char

    return bitmaskToTile


def convert_level(map, mask, bitmaskToTile, bitmask_finder):
    # copy the map to convert it
    map_to_convert = [r[:] for r in map]

    # run bitmask for all relevant tiles
    for y in range(len(map_to_convert)):
        for x in range(len(map_to_convert[0])):
            if not mask[y][x]:
                continue

            bitmask = bitmask_finder(mask, x, y)
            if bitmask in bitmaskToTile:
                map_to_convert[y][x] = bitmaskToTile[bitmask]

    # map is now converted
    return map_to_convert
