with open(0, encoding="utf-8") as f:
    D = f.read()

raw_vectors = [line.split(" @ ") for line in D.splitlines()]


vectors = [
    tuple([tuple([int(z) for z in y.split(", ")]) for y in x]) for x in raw_vectors
]


def check_intersection(mx1, mx2, my1, my2):
    return 0 != mx1 * -my2 + mx2 * my1


def find_intersection(first, sec, min_test, max_text):
    pos, vec = first
    bx1, by1, bz1 = pos
    mx1, my1, mz1 = vec

    sec_pos, sec_vec = sec
    bx2, by2, bz2 = sec_pos
    mx2, my2, mz2 = sec_vec

    if check_intersection(mx1, mx2, my1, my2):
        mod = 1 / (mx1 * -my2 + mx2 * my1)
        s = (-my2 * bx1 + my1 * bx2) * mod
        t = (mx1 * -by2 + mx2 * by1) * mod

        x, y = mx1 * t + bx1, my1 * t + by1
        print("intersection:", first, sec, x, y)
        if min_test <= x <= max_test and min_test <= y <= max_text:
            print("inside test")


# x, y, z


test = lambda x, px, py, pz, vx, vy, vz: [
    vx * x + px,
    vy * x + py,
    vz * x + pz,
]

min_test, max_test = 7, 27

check_seen = set()
formulas = []
# x, y, z
for first in vectors:
    pos, vec = first
    bx1, by1, bz1 = pos
    mx1, my1, mz1 = vec
    print("P:", pos, vec)

    for sec in vectors:
        key = tuple(sorted((first, sec)))
        if first != sec and key not in check_seen:
            check_seen.add(key)
            sec_pos, sec_vec = sec
            find_intersection(first, sec, min_test, max_test)
