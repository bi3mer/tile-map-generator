def hamming_distance(a, b, bits):
    sim = 0

    for i in range(bits):
        sim += int((a >> i) & 1 != (b >> i) & 1)

    return sim


# Function assumes that top annd bottom rows are not relevant. Same for
# left and right columns.
# 1 2 3
# 4 * 5
# 6 7 8
def __get_separated_mask(map, x, y):
    H = len(map) - 1
    W = len(map[0]) - 1

    NW = map[y - 1][x - 1] if y > 0 and x > 0 else True
    N = map[y - 1][x] if y > 0 else True
    NE = map[y - 1][x + 1] if y > 0 and x < W else True
    W = map[y][x - 1] if x > 0 else True
    E = map[y][x + 1] if x < W else True
    SW = map[y + 1][x - 1] if y < H and x > 0 else True
    S = map[y + 1][x] if y < H else True
    SE = map[y + 1][x + 1] if y < H and x < W else True

    return NW, N, NE, W, E, SW, S, SE


def __bit_mask(NW, N, NE, W, E, SW, S, SE):
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


def get_bit_mask(map, x, y):
    return __bit_mask(*__get_separated_mask(map, x, y))


# Function assumes that top annd bottom rows are not relevant. Same for
# left and right columns.
# 1 2 3
# 4 * 5
# 6 7 8
def get_bit_mask_ignore_corners(map, x, y):
    NW, N, NE, W, E, SW, S, SE = __get_separated_mask(map, x, y)

    if not (N and W):
        NW = False
    if not (N and E):
        NE = False
    if not (S and W):
        SW = False
    if not (S and E):
        SE = False

    return __bit_mask(NW, N, NE, W, E, SW, S, SE)


def large_bit_mask(map, x, y):
    H = len(map)
    W = len(map[0])

    bit_index = 0
    mask = 0

    for _y in range(y - 2, y + 3):
        _y_condition = _y >= 0 and _y < H
        for _x in range(x - 2, x + 3):
            if _x == x and _y == y:
                continue  # skip origin

            mask |= (
                map[_y][_x] if _y_condition and _x >= 0 and _x < W else True
            ) << bit_index

            bit_index += 1

    return mask
