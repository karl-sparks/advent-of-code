"""AOC day 8"""

from collections import defaultdict
from itertools import combinations
import math

print("AOC day 8")
fp_0 = "data/test.txt"
fp_1 = "data/day-8.txt"

with open(fp_1, encoding="utf-8") as f:
    D = [x.strip() for x in f.readlines()]

max_x, max_y = len(D), len(D[0])

def get_sym(D):
    syms = defaultdict(lambda: set())
    for x, line in enumerate(D):
        for y, c in enumerate(line):
            if c != ".":
                syms[c].add((x, y))
    return syms

def ans_1(D):
    ans = 0
    
    uni_loc = set()
    
    syms = get_sym(D)

    for key, values in syms.items():
        for left, right in list(combinations(values, r = 2)):
            assert left != right
            xl, yl = left
            xr, yr = right
            
            x_dist = abs(xl - xr)
            y_dist = abs(yl - yr)
            
            if xl < xr:
                nx1 = xl - x_dist
                nx2 = xr + x_dist
            else: 
                nx1 = xl + x_dist
                nx2 = xr - x_dist
                
            if yl < yr:
                ny1 = yl - y_dist
                ny2 = yr + y_dist
            else:
                ny1 = yl + y_dist
                ny2 = yr - y_dist
                
            if 0 <= nx1 < max_x and 0 <= ny1 < max_y:
                uni_loc.add((nx1, ny1))

            if 0 <= nx2 < max_x and 0 <= ny2 < max_y:
                uni_loc.add((nx2, ny2))
    
    ans = len(uni_loc)
    
    return ans

print(f"Ans 1: {ans_1(D)}")


def ans_2(D):
    ans = 0

    uni_loc = set()
    
    uni_eq = set()
    
    syms = get_sym(D)
    
    #y = mx + b
    
    for key, values in syms.items():
        for left, right in list(combinations(values, r = 2)):
            x1, y1 = left
            x2, y2 = right
    
            assert (x1 != x2)
            m = (y2 - y1) / (x2 - x1)
            b = (y1 - m * x1)
            
            uni_eq.add((m, b))
            
            
    for x in range(max_x):
        for y in range(max_y):
            for m, b in uni_eq:
                if abs(y - (x*m + b)) < 0.0000001:
                    uni_loc.add((x, y))
    
    ans = len(uni_loc)
    return ans

print(f"Ans 2: {ans_2(D)}")