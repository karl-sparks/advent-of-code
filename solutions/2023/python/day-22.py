from functools import cache

with open(0, encoding="utf-8") as f:
    D = f.read()

brick_input = [
    [[int(coord) for coord in coords.split(",")] for coords in row.split("~")]
    for row in D.splitlines()
]

max_x = max([brick[1][0] for brick in brick_input])
max_y = max([brick[1][1] for brick in brick_input])
max_z = max([brick[1][2] for brick in brick_input])

grid = [
    [[0 for _ in range(max_z + 1)] for _ in range(max_y + 1)] for _ in range(max_x + 1)
]

for i, brick in enumerate(brick_input):
    b_id = i + 1
    start_b, end_b = brick
    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            for z in range(start_b[2], end_b[2] + 1):
                grid[x][y][z] = b_id


def move_brick(b_id, start_b, end_b):
    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            for z in range(start_b[2], end_b[2] + 1):
                grid[x][y][z] = 0

    start_b[2] -= 1
    end_b[2] -= 1

    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            for z in range(start_b[2], end_b[2] + 1):
                grid[x][y][z] = b_id


def check_collesion(b_id, start_b, end_b, ignore_id=None):
    if ignore_id is None:
        ignore_id = b_id
    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            lowest_z = min(start_b[2], end_b[2]) - 1
            if lowest_z <= 0 or grid[x][y][lowest_z] not in [0, ignore_id]:
                return True
    return False


def check_collesion_return_ids(b_id, start_b, end_b, ignore_id=None, return_ids=None):
    if ignore_id is None:
        ignore_id = b_id

    if return_ids is None:
        return_ids = set()

    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            highest_z = end_b[2] + 1
            if highest_z < max_z:
                if grid[x][y][highest_z] not in [0, ignore_id]:
                    return_ids.add(grid[x][y][highest_z])

    return return_ids


def check_for_falling_bricks():
    moved_bricks = False
    for i, brick in enumerate(brick_input):
        b_id = i + 1
        collesion = False
        start_b, end_b = brick

        if not check_collesion(b_id, start_b, end_b):
            move_brick(b_id, start_b, end_b)
            moved_bricks = True

    return moved_bricks


moved_bricks = True
while moved_bricks:
    moved_bricks = check_for_falling_bricks()


cache = {}


def check_brick_for_falling(check_id, all_ids):
    if check_id in cache:
        return cache[check_id]

    start_b, end_b = brick_input[check_id - 1]

    all_ids.update(check_collesion_return_ids(check_id, start_b, end_b))

    cache[check_id] = all_ids

    return all_ids


class brick_obj:
    def __init__(self, b_id, supports, rest_on):
        self.b_id = b_id
        self.supports = supports
        self.rest_on = rest_on


brick_map = {}

for i, brick in enumerate(brick_input):
    b_id = i + 1

    supports = list(check_brick_for_falling(b_id, set()))

    rest_on = []

    brick_map[b_id] = brick_obj(b_id, supports, rest_on)

for k, v in brick_map.items():
    for s_id in v.supports:
        brick_map[s_id].rest_on.append(k)


def get_support_count(b_id, removed_ids):
    b = brick_map[b_id]

    if removed_ids is not None and not set(b.rest_on).issubset(removed_ids):
        return set()

    if removed_ids is None:
        removed_ids = set([b_id])
    else:
        removed_ids.add(b_id)

    for s_id in b.supports:
        get_support_count(s_id, removed_ids)

    return removed_ids


test_safe = set()
not_safe_ids = set()

for i in range(len(brick_input)):
    b_id = i + 1
    b = brick_map[b_id]

    b_id_check = [b_id]
    safe = True
    for s_id in b.supports:
        if b_id_check == brick_map[s_id].rest_on:
            safe = False
            break

    if safe:
        test_safe.add(b_id)
    else:
        not_safe_ids.add(b_id)


ans_1 = len(test_safe)
ans_2 = 0
for b_id in not_safe_ids:
    num_f_b = get_support_count(b_id, None)
    ans_2 += len(num_f_b) - 1

print("Part 1:", ans_1)
print("Part 2:", ans_2)
