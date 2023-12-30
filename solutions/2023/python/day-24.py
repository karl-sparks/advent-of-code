import numpy as np
import heapq

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


def closest_approach(first, sec):
    P1 = np.array([*first[0]])
    V1 = np.array([*first[1]])
    P2 = np.array([*sec[0]])
    V2 = np.array([*sec[1]])

    A = np.array([V1, -V2]).T

    if np.linalg.matrix_rank(A) < 2:
        return None

    B = P2 - P1
    X, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
    assert len(X) == 2, f"Should be 2 {X}"

    if np.all(X >= 0):
        i1 = P1 + X[0] * V1
        i2 = P2 + X[1] * V2

        return np.linalg.norm(i1 - i2)

    return None


ans_2 = 0

possible_search_path = [
    (1, 0, 0, 0, 0, 0),
    (-1, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 0),
    (0, -1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0),
    (0, 0, -1, 0, 0, 0),
]

possible_values = [(1e9, 24, 13, 10, -3, 1, 2)]

heapq.heapify(possible_values)

# Find least squared errors:
while True:
    score, nx, ny, nz, nmx, nmy, nmz = heapq.heappop(possible_values)

    first = [(nx, ny, nz), (nmx, nmy, nmz)]

    errors = 0
    
    miss_int = False
    for i in range(12):
        modify_vect = [0]*6
        new_vec = modify_vect[i%2][i%3] + (-1)**(i//6)

        test_line = ((nx + new_vec[0], ny + new_vec[1], nz + new_vec[2]),
                (nmx + new_vec[3], nmy + new_vec[4], nmz + new_vec[5]))

        for sec in vectors_p2:
            match closest_approach(first, sec):
                case None:
                    miss_int = True
                case float(x):
                    errors += x

        if not miss_int:
            ans_2 = (nx + ny + nz)
                    
        heapq.heappush(possible_values, (score, ))

    print("errors:", errors)


print("Part 2:", ans_2)
