"""AOC day 16"""
from collections import deque
from importlib.resources import path
from itertools import product

import heapq

num_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["NONE", "0", "A"]
]

ro_keypad = [
    ["NONE", "^", "A"],
    ["<", "v", ">"]
]

ro_dirs = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}

num_pos = {}
ro_pos = {}

for r in range(len(num_keypad)):
    for c in range(len(num_keypad[r])):
        if num_keypad[r][c] != "NONE":
            num_pos[num_keypad[r][c]] = (r, c)

for r in range(len(ro_keypad)):
    for c in range(len(ro_keypad[r])):
        if ro_keypad[r][c] != "NONE":
            ro_pos[ro_keypad[r][c]] = (r, c)

cached_seq = {}

def find_seq(start: tuple[int, int], end: tuple[int, int], pos: dict, depth: int) -> set:
    """Find sequence from start to end"""
    if start == end:
        return set(["A"])
    if (start, end, depth) in cached_seq:
        return cached_seq[(start, end, depth)]

    q = deque([(start, "")]) 
    opt_dist = float("inf")
    possibilities = set()
    while q:
        (r, c), path = q.popleft()
        for nr, nc, nm in [(r - 1, c, path + "^"), (r + 1, c, path + "v"), (r, c - 1, path + "<"), (r, c + 1, path + ">")]:
            if (nr, nc) not in pos.values():
                continue
            if (nr, nc) == end:
                if opt_dist < len(nm): break
                opt_dist = len(nm)
                possibilities.add(nm + "A")
            else:
                q.append(((nr, nc), nm))
        else:
            continue
        break
    
    if depth > 0:
        new_possibilities = set()
        for seq in possibilities:
            new_possibilities.update(set(convert_seq_to_command(seq, ro_pos, depth - 1)))
                
        possibilities = new_possibilities

    cached_seq[(start, end, depth)] = possibilities

    return cached_seq[(start, end, depth)]

def convert_seq_to_command(input_seq: str, pos: dict, depth: int) -> list[str]:
    return_seq = []
    for i in range(len(input_seq)):
        if i == 0:
            seq = find_seq(pos["A"], pos[input_seq[i]], pos, depth)
        else:
            seq = find_seq(pos[input_seq[i - 1]], pos[input_seq[i]], pos, depth)
        return_seq.append(seq)
        
    return list("".join(x) for x in product(*return_seq))

def part_one(data: str) -> int:
    return_ans = 0
    for line in D.splitlines():
        ans = convert_seq_to_command(line, num_pos, 2)
        min_seq = min([len(x) for x in ans])
        return_ans += int(line[0:3]) * min_seq
    
    return return_ans
    
cached_seq_flat = {}

def find_seq_flat(start: tuple[int, int], end: tuple[int, int], input_pos: dict, is_num_pos: bool) -> set:
    """Find sequence from start to end"""
    if start == end:
        return set(["A"])
    if (start, end, is_num_pos) in cached_seq_flat:
        return cached_seq_flat[(start, end, is_num_pos)]

    q = deque([(start, "")]) 
    opt_dist = float("inf")
    possibilities = set()
    while q:
        (r, c), path = q.popleft()
        for nr, nc, nm in [(r - 1, c, path + "^"), (r + 1, c, path + "v"), (r, c - 1, path + "<"), (r, c + 1, path + ">")]:
            if (nr, nc) not in input_pos.values():
                continue
            if (nr, nc) == end:
                if opt_dist < len(nm): break
                opt_dist = len(nm)
                possibilities.add(nm + "A")
            else:
                q.append(((nr, nc), nm))
        else:
            continue
        break

    cached_seq_flat[(start, end, is_num_pos)] = possibilities

    return cached_seq_flat[(start, end, is_num_pos)]

numpad_paths = {(start, end): find_seq_flat(num_pos[start], num_pos[end], num_pos, True) for start in num_pos for end in num_pos}
dirpad_paths = {(start, end): find_seq_flat(ro_pos[start], ro_pos[end], ro_pos, False) for start in ro_pos for end in ro_pos}

def code_to_paths(keypad_paths: dict, code: str) -> list[str]:
    paths = [keypad_paths[(start, end)] for start, end in zip("A" + code, code)]

    return ["".join(x) for x in product(*paths)]

min_path_cache = {}

def get_min_length(code: str, depth: int) -> int:
    if (code, depth) in min_path_cache:
        return min_path_cache[(code, depth)]
    
    if depth == 0:
        return len(code)

    min_length = 0
    for start, end in zip("A" + code, code):
        min_length += min(get_min_length(seq, depth - 1) for seq in dirpad_paths[(start, end)])

    min_path_cache[(code, depth)] = min_length

    return min_path_cache[(code, depth)]

def part_two(data: str) -> int:
    return_ans = 0
    for line in data.splitlines():
        ans = float("inf")
        for path in code_to_paths(numpad_paths, line):
            ans = min(get_min_length(path, 25), ans)
        return_ans += int(line[0:3]) * ans
    
    return return_ans


if __name__ == "__main__":
    print("AOC day 21")
    with open(0, encoding="utf-8") as f:
        D = f.read()
    print("Part one: ", part_one(D))
    print("Part two: ", part_two(D))
