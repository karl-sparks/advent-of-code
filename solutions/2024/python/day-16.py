"""AOC day 16"""

from dataclasses import dataclass

print("AOC day 16")
fp_0 = "data/test-16.txt"
fp_1 = "data/day-16.txt"

def read_input(input):
    with open(input, encoding="utf-8") as f:
        D = [x.strip() for x in f.readlines()]

    return D

def parse_map(D):
    return [[x for x in line] for line in D]

def get_start(p_map):
    for x, line in enumerate(p_map):
        for y, c in enumerate(line):
            if c == "S":
                return (x, y)


df = {
    "N": (-1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "S": (1, 0)
}

cd = {
    "N": "WNE",
    "E": "NES",
    "S": "ESW",
    "W": "NWS"
}

@dataclass(order=True)
class Path():
    x: int
    y: int
    d: str
    path: set

def search_map(start, p_map):
    start_p = Path(start[0], start[1], d="E", path=set([start]))
    
    que = [(0, start_p)]
    
    valid_paths = set()
    best_score = 1_000_000
    
    pos_scores = {}
    pos_scores[start] = 0
    
    while que:
        que.sort()
        score, np = que.pop(0)
        if score > pos_scores.get((np.x, np.y, np.d), best_score):
            continue
        
        pos_scores[(np.x, np.y, np.d)] = min(pos_scores.get((np.x, np.y, np.d), score), score)
        
        pos = p_map[np.x][np.y]
        
        if pos == "E" and best_score == 1_000_000:
            best_score = score
            valid_paths.update(np.path)
        elif pos == "E":
            assert score == best_score
            valid_paths.update(np.path)
        else:
            for new_d in cd[np.d]:
                nx = np.x + df[new_d][0]
                ny = np.y + df[new_d][1]
                if 0 <= nx < len(p_map) and 0 <= ny < len(p_map[0]) and (nx, ny) not in np.path:
                    n_pos = p_map[nx][ny]
                    if n_pos != "#":
                        n_path = np.path.copy()
                        n_path.add((nx, ny))
                        
                        scor_adj = 1 if np.d == new_d else 1001
                        
                        new_score = score + scor_adj

                        if new_score <= pos_scores.get((nx, ny, new_d), best_score):
                            que.append((new_score, Path(x=nx, y=ny, d=new_d, path=n_path)))
    
    return best_score, len(valid_paths)           


def ans_1(D):
    ans = 0

    p_map = parse_map(D)
    start = get_start(p_map)
    
    ans = search_map(start, p_map)
    
    return ans


print(f"Ans 1 and 2 test: {ans_1(read_input(fp_0))}")
print(f"Ans 1 and 2 real: {ans_1(read_input(fp_1))}\n")

def ans_2(D):
    ans = 0
    
    return ans


#print(f"Ans 2 test: {ans_2(read_input(fp_0))}")
#print(f"Ans 2 real: {ans_2(read_input(fp_1))}")