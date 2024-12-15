"""AOC day 15"""

import os
import time

print("AOC day 15")
fp_0 = "data/test-15.txt"
fp_1 = "data/day-15.txt"

def read_input(input):
    with open(input, encoding="utf-8") as f:
        D = [x.strip() for x in f.readlines()]

    return D

def parse_area(D):
    for i in range(len(D)):
        if D[i] == "":
            return [[x for x in line] for line in D[:i]], i

dt = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
    "[": (0, 1),
    "]": (0, -1)
}

def get_robot_pos(area):
    for x, line in enumerate(area):
        for y, c in enumerate(line):
            if c == "@":
                return x, y
    assert False

def mp(start, instr):
    xm, ym = dt[instr]
    return start[0] + xm, start[1] + ym

def move_robot(start, instr, area):    
    np = mp(start, instr)
    
    np_c = area[np[0]][np[1]]
    
    if np_c == "#":
        return
    elif np_c  == ".":
        area[np[0]][np[1]] = area[start[0]][start[1]]
        area[start[0]][start[1]] = "."
        return
    elif np_c == "O":
        move_robot(np, instr, area)
        area[np[0]][np[1]] = area[start[0]][start[1]]
        area[start[0]][start[1]] = "."
        return
    elif np_c in "[]":
        move_robot(np, instr, area)
        area[np[0]][np[1]] = area[start[0]][start[1]]
        area[start[0]][start[1]] = "."
        if instr in "^v":
            move_robot(mp((start[0] + dt[np_c][0], start[1] + dt[np_c][1]), instr), instr, area)
        return
    assert False, np_c
    
def can_move(start, instr, area):
    np = mp(start, instr)
    
    np_c = area[np[0]][np[1]]
    
    if np_c == "#":
        return False
    elif np_c  == ".":
        return True
    elif np_c == "O":
        return can_move(np, instr, area)
    elif np_c in "[]":
        moved = can_move(np, instr, area)
                                                           
        if instr in "^v":
            moved = moved and can_move(mp((start[0] + dt[np_c][0], start[1] + dt[np_c][1]), instr), instr, area)
        
        return moved
    assert False, np_c

def ans_1(D):
    ans = 0

    area, brk = parse_area(D)
    
    insts = D[brk + 1:]
    
    start = get_robot_pos(area)

    for line in insts:
        for inst in line:
            if can_move(start, inst, area):
                move_robot(start, inst, area)
                start = mp(start, inst)

    for x, line in enumerate(area):
        for y, c in enumerate(line):
            if c == "O":
                ans += 100 * x + y
    
    return ans

print(f"Ans 1 test: {ans_1(read_input(fp_0))}")
print(f"Ans 1 real: {ans_1(read_input(fp_1))}\n")

split_rules = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@."
}

def parse_area_2(D):
    return_i = 0
    for i in range(len(D)):
        if D[i] == "":
            area = [[split_rules[x] for x in line] for line in D[:i]]
            return_i = i
            break

    return [[char for string in line for char in string] for line in area], return_i
            

def ans_2(D):
    ans = 0
    
    area, brk = parse_area_2(D)
    
    insts = D[brk + 1:]
    
    num_instrs = len(insts) * len(insts[0])
    
    start = get_robot_pos(area)
    
    width = len(area[0]) + 1

    procsesed_insts = 0

    os.system("clear")
    time.sleep(3)

    for line in insts:
        for inst in line:
            if can_move(start, inst, area):
                move_robot(start, inst, area)
                start = mp(start, inst)
            os.system("clear")
            procsesed_insts += 1
            for t in area:
                print("".join(t))
            print("="*int(width*(procsesed_insts/num_instrs)) + "+"*int(width*(1-(procsesed_insts/num_instrs))))
            time.sleep(0.01)

    for x, line in enumerate(area):
        for y, c in enumerate(line):
            if c == "[":
                ans += 100 * x + y
    
    return ans


#print(f"Ans 2 test: {ans_2(read_input(fp_0))}")
print(f"Ans 2 real: {ans_2(read_input(fp_1))}")