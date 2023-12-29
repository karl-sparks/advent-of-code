with open(0, encoding="utf-8") as f:
    D = f.read()

raw_vectors = [line.split(" @ ") for line in D.splitlines()]


vectors = [
    tuple([tuple([int(z) for z in y.split(", ")]) for y in x]) for x in raw_vectors
]


def check_intersection(mx1, mx2, my1, my2):
    return 0 != mx1 * -my2 + mx2 * my1


# x, y, z


def find_intersection(first, sec, min_test, max_test):
    pos, vec = first
    bx1, by1, bz1 = pos
    mx1, my1, mz1 = vec

    sec_pos, sec_vec = sec
    bx2, by2, bz2 = sec_pos
    mx2, my2, mz2 = sec_vec

    if check_intersection(mx1, mx2, my1, my2):
        mod = 1 / (mx1 * -my2 + mx2 * my1)
        s = ((bx1 - bx2) * my1 - (by1 - by2) * mx1) * mod
        t = ((bx1 - bx2) * my2 - (by1 - by2) * mx2) * mod

        xs, ys = mx2 * s + bx2, my2 * s + by2
        xt, yt = mx1 * t + bx1, my1 * t + by1
        if (
            min_test <= xs <= max_test
            and min_test <= ys <= max_test
            and s >= 0
            and t >= 0
        ):
            return 1
    return 0


# x, y, z
test = lambda x, px, py, pz, vx, vy, vz: [
    vx * x + px,
    vy * x + py,
    vz * x + pz,
]

if len(vectors) <= 20:
    min_test, max_test = 7, 27
else:
    min_test, max_test = 200000000000000, 400000000000000

check_seen = set()
formulas = []
# x, y, z
ans_1 = 0
for first in vectors:
    pos, vec = first
    bx1, by1, bz1 = pos
    mx1, my1, mz1 = vec

    for sec in vectors:
        key = tuple(sorted((first, sec)))
        if first != sec and key not in check_seen:
            check_seen.add(key)
            sec_pos, sec_vec = sec
            ans_1 += find_intersection(first, sec, min_test, max_test)

print("Part 1:", ans_1)

ans_2 = 0


print("Part 2:", ans_2)
