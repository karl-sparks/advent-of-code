import numpy as np
import sympy

with open(0, encoding="utf-8") as f:
    D = f.read()

raw_vectors = [line.split(" @ ") for line in D.splitlines()]

vectors_p1 = [
    tuple([tuple([int(z) for z in y.split(", ")]) for y in x]) for x in raw_vectors
]

vectors_p1 = [tuple([x[:2] for x in y]) for y in vectors_p1]

vectors_p2 = [
    tuple([tuple([int(z) for z in y.split(", ")]) for y in x]) for x in raw_vectors
]


def find_intersection(first, sec):
    P1 = np.array([*first[0]])
    V1 = np.array([*first[1]])
    P2 = np.array([*sec[0]])
    V2 = np.array([*sec[1]])

    A = np.array([V1, -V2]).T

    if np.linalg.matrix_rank(A) < 2:
        return None

    B = P2 - P1
    X = np.linalg.solve(A, B)

    if np.all(X >= 0):
        i1 = P1 + X[0] * V1
        i2 = P2 + X[1] * V2

        return i1

    return None


def find_intersection_p1(first, sec, min_test, max_test):
    X = find_intersection(first, sec)

    if X is not None and np.all(X >= min_test) and np.all(X <= max_test):
        return 1
    return 0


if len(vectors_p1) <= 20:
    min_test, max_test = 7, 27
else:
    min_test, max_test = 200000000000000, 400000000000000

check_seen = set()

ans_1 = 0

for first in vectors_p1:
    for sec in vectors_p1:
        key = tuple(sorted((first, sec)))
        if first != sec and key not in check_seen:
            check_seen.add(key)
            ans_1 += find_intersection_p1(first, sec, min_test, max_test)

print("Part 1:", ans_1)


# For a rock to hit a stone, we would need to find a pos and vector for the rock that would equal the stone pos/vec after a given t
# e.g. for the x coordinate; xr + xdr * t = xs + xds * t
# Rearrange for t lets us sets up a series of equations to equat all axis
# t = (xs - xr)/(xdr - xds)
# This is the same format for each axis. Therefore:
# (xs - xr)/(xdr - xds) = (ys - yr) / (ydr - yds) = (zs - zr) / (zdr - zds)
# We can simplify to two equations to solve for each combination of 'rock' and stone
# x by y; and
# y by z;
# E.g.
# (xs - xr)*(ydr - yds) - (ys - yr)*(xdr - xds) = 0
# (ys - yr)*(zdr - zds) - (zs - zr)*(ydr - yds) = 0
# we then go through each hailstone and add this two equations and solve using sympy
def solve_part2(stones):
    xr, yr, zr, xdr, ydr, zdr = sympy.symbols("xr, yr, zr, xdr, ydr, zdr")
    equations = []

    for i, (pos, vec) in enumerate(stones):
        xs, ys, zs = pos
        xds, yds, zds = vec
        equations.append((xs - xr) * (ydr - yds) - (ys - yr) * (xdr - xds))
        equations.append((ys - yr) * (zdr - zds) - (zs - zr) * (ydr - yds))

        if i >= 2:
            answer = sympy.solve(equations)
            if len(answer) == 1:
                print(f"solved with {i + 1} hailstones out of {len(stones)}")
                break

    assert len(answer) == 1, "Should only have one solution"
    assert all(
        x % 1 == 0 for x in answer[0].values()
    ), "Solution should be interger values"

    return answer[0][xr] + answer[0][yr] + answer[0][zr]


ans_2 = solve_part2(vectors_p2)

print("Part 2:", ans_2)
