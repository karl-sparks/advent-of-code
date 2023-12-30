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

possible_values = [(1e9, (0, 0, 0), (1, 1, 1))]

heapq.heapify(possible_values)

seen = set()

attempts = 0
while True:
    score, pos, vec = heapq.heappop(possible_values)
    seen.add((pos, vec))
    nx, ny, nz = pos
    nmx, nmy, nmz = vec
    min_error = score
    print(
        "Checking:",
        attempts,
        ((nx, ny, nz), (nmx, nmy, nmz)),
        score,
        len(possible_values),
    )

    for i in range(12):
        modify_vect = [0] * 6
        modify_vect[i % 6] += (-1) ** (i // 6)

        test_line = (
            (nx + modify_vect[0], ny + modify_vect[1], nz + modify_vect[2]),
            (nmx + modify_vect[3], nmy + modify_vect[4], nmz + modify_vect[5]),
        )

        errors = 0

        for sec in vectors_p2:
            match closest_approach(test_line, sec):
                case None:
                    errors += 1e9
                case float(x):
                    errors += x

        if test_line not in seen:
            min_error = min(errors, min_error)
            heapq.heappush(possible_values, (errors, *test_line))

    if score <= errors:
        attempts += 1

    if attempts > 100000:
        _, final_pos, _ = heapq.heappop(possible_values)
        ans_2 = sum(final_pos)
        break


print("Part 2:", ans_2)
