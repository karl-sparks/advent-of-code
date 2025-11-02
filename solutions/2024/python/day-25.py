def get_heights(things: list[list[str]]) -> list[list[int]]:
    heights: list[list[int]] = []
    for thing in things:
        height = [-1 for _ in range(len(thing[0]))]
        for i in range(len(thing[0])):
            for k in range(len(thing)):
                if thing[k][i] == "#":
                    height[i] += 1
        heights.append(height)
    return heights


def does_key_fit(key: list[int], lock: list[int]) -> bool:
    return all(k + i <= 5 for k, i in zip(key, lock))


def parse_d(D: str) -> tuple[list[list[int]], list[list[int]]]:
    split_D = [x.split() for x in D.split("\n\n")]

    locks = [x for x in split_D if x[0] == "#####"]
    keys = [x for x in split_D if x[6] == "#####"]

    lock_heights = get_heights(locks)
    key_heights = get_heights(keys)

    assert len(locks) + len(keys) == len(split_D)
    assert len(locks) == len(lock_heights)
    assert len(keys) == len(key_heights)

    return lock_heights, key_heights


def part_one(locks: list[list[int]], keys: list[list[int]]) -> int:
    ans = 0
    print("Checking locks")
    for key in keys:
        for lock in locks:
            if does_key_fit(key, lock):
                ans += 1

    return ans


if __name__ == "__main__":
    print("AOC day 25")
    with open(0, encoding="utf-8") as f:
        D = f.read()

    locks, keys = parse_d(D)

    print("Answer part one: ", part_one(locks, keys))
