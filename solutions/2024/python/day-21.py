"""AOC day 16"""
from collections import deque

num_keypad = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    ["NONE", 0, "A"]
]

ro_keypad = [
    ["NONE", "^", "A"],
    ["<", "v", ">"]
]

pos = {}

for r in range(len(num_keypad)):
    for c in range(len(num_keypad[r])):
        if num_keypad[r][c] != "NONE":
            pos[num_keypad[r][c]] = (r, c)

print(pos)

cached_seq = {}

def find_seq(start: (int, int), end: (int, int)) -> set:
    """Find sequence from start to end"""
    if start == end:
        return set(["A"])
    if (start, end) in cached_seq:
        return cached_seq[(start, end)]

    q = deque([(start, "")]) 
    opt_dist = float("inf")
    possibilities = []
    while q:
        print(q)
        (r, c), path = q.popleft()
        for nr, nc, nm in [(r - 1, c, path + "^"), (r + 1, c, path + "v"), (r, c - 1, path + "<"), (r, c + 1, path + ">")]:
            if (nr, nc) not in pos:
                continue
            if (nr, nc) == end:
                if opt_dist < len(nm): break
                opt_dist = len(nm)
                possibilities.append(nm)
            else:
                print("adding to q", q)
                q.append(((nr, nc), nm))
        else:
            continue
        break
            
    cached_seq[(start, end)] = set(possibilities)

    return cached_seq[(start, end)]

print(find_seq((2, 1), (2, 1)))
print(find_seq((3, 1), (0, 2)))

def part_one(data: str) -> int:
    for line in D.splitlines():
        print(line)

if __name__ == "__main__":
    with open(0, encoding="utf-8") as f:
        D = f.read()
    part_one(D)