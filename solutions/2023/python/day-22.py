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

print(max_x, max_y, max_z)

for i, brick in enumerate(brick_input):
    b_id = i + 1
    start_b, end_b = brick
    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            for z in range(start_b[2], end_b[2] + 1):
                grid[x][y][z] = b_id

for line in grid:
    print(line)


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


def check_collesion(b_id, start_b, end_b):
    for x in range(start_b[0], end_b[0] + 1):
        for y in range(start_b[1], end_b[1] + 1):
            lowest_z = min(start_b[2], end_b[2]) - 1
            if lowest_z <= 0 or grid[x][y][lowest_z] != 0:
                return True
    return False


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

for i, brick in enumerate(brick_input):
    b_id = i + 1

print("=" * 50)

for line in grid:
    print(line)
