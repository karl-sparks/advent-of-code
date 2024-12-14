"""AOC day 12"""

from collections import defaultdict
from itertools import combinations
import math

print("AOC day 12")
fp_0 = "data/test.txt"
fp_1 = "data/day-12.txt"

def read_input(input):
    with open(input, encoding="utf-8") as f:
        D = [x.strip() for x in f.readlines()]

    return D
    


def find_plot(spot, prev_spot, areas, connections, D):
    x, y = spot
    px, py = prev_spot
    max_x, max_y = len(D), len(D[0])
   
    if not (0 <= x < max_x) or not (0 <= y < max_y):
        return
   
    if spot != prev_spot and D[x][y] != D[px][py]:
        return
    
    areas.add(spot)

    if spot != prev_spot:
        
        assert D[x][y] == D[px][py]
        con = [spot, prev_spot]
        con.sort()
        con = tuple(con)
        if con in connections:
            return
        connections.add(con)
    

    for mx, my in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        find_plot((mx + x, my + y), spot, areas, connections, D)

    return


def ans_1(D):
    max_x, max_y = len(D), len(D[0])
    ans = 0
    
    checked_areas = set()
    
    for x in range(max_x):
        for y in range(max_y):
            spot = (x, y)
            if spot not in checked_areas:
                areas = set()
                connections = set()
                find_plot(spot, spot, areas, connections, D)
                checked_areas.update(areas)
                ans += len(areas) * (len(areas) * 4 - len(connections) * 2)
    
    return ans

print(f"Ans 1 test: {ans_1(read_input(fp_0))}\n")
print(f"Ans 1 real: {ans_1(read_input(fp_1))}\n")

def ans_2_pre(D):
    ans = 0

    max_x, max_y = len(D) * 2, len(D[0]) * 2

    new_D = [["" for _ in range(max_y-1)] for _ in range(max_x-1)]
    
    for x, row in enumerate(D):
        for y, c in enumerate(row):
            new_D[x*2][y*2] = c
    
    test = "R"
    
    for x, row in enumerate(new_D):
        for y, c in enumerate(row):
            if not x % 2 and c == "":
                if new_D[x][y-1] != new_D[x][y+1]:
                    new_D[x][y] = "".join(sorted(new_D[x][y-1] + new_D[x][y+1]))
            elif x % 2 == 1 and not y % 2:
                if new_D[x-1][y] != new_D[x+1][y]:
                    new_D[x][y] = "".join(sorted(new_D[x-1][y] + new_D[x+1][y]))
    
    return ans


print(f"Ans 2 test: {ans_2(read_input(fp_0))}\n")
#print(f"Ans 2 real: {ans_2(read_input(fp_1))}\n")