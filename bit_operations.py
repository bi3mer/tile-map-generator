# Function assumes that top annd bottom rows are not relevant. Same for
# left and right columns.
# 1 2 3
# 4 * 5
# 6 7 8
def get_bit_mask(map, x, y):
    res = 0
    res |= map[y - 1][x - 1]
    res |= map[y - 1][x] << 1
    res |= map[y - 1][x + 1] << 2
    res |= map[y][x - 1] << 3
    res |= map[y][x + 1] << 4
    res |= map[y + 1][x - 1] << 5
    res |= map[y + 1][x] << 6
    res |= map[y + 1][x + 1] << 7

    return res


# Function assumes that top annd bottom rows are not relevant. Same for
# left and right columns.
# 1 2 3
# 4 * 5
# 6 7 8
def get_bit_mask_ignore_corners(map, x, y):
    NW = map[y - 1][x - 1]
    N = map[y - 1][x]
    NE = map[y - 1][x + 1]
    W = map[y][x - 1]
    E = map[y][x + 1]
    SW = map[y + 1][x - 1]
    S = map[y + 1][x]
    SE = map[y + 1][x + 1]

    if not (N and W):
        NW = False
    if not (N and E):
        NE = False
    if not (S and W):
        SW = False
    if not (S and E):
        SE = False

    res = 0
    res |= NW
    res |= N << 1
    res |= NE << 2
    res |= W << 3
    res |= E << 4
    res |= SW << 5
    res |= S << 6
    res |= SE << 7

    return res
