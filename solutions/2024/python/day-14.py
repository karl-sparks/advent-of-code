"""AOC day 14"""

from dataclasses import dataclass

print("AOC day 14")
fp_0 = "data/test-14.txt"
fp_1 = "data/day-14.txt"

@dataclass
class Robot:
    x: int
    y: int
    vol_x: int
    vol_y: int

def read_input(input):
    with open(input, encoding="utf-8") as f:
        D = [x.strip() for x in f.readlines()]

    return D

def parse_left(left: str) -> int:
    return int(left[left.index("=") + 1:])

def parse_robots(line):
    pos, vol = line.split(" ")
    
    left, right = pos.split(",")
    x = parse_left(left)
    y = int(right)
    
    left, right = vol.split(",")
    vol_x = parse_left(left)
    vol_y = int(right)

    return Robot(x, y, vol_x, vol_y)

def print_robots(robots):
    maps = [[0 for _ in range(101)] for _ in range(103)]
    
    print(len(maps), len(maps[0]))
    
    for robot in robots:
        maps[robot.y][robot.x] += 1
        
    for line in maps:
        print("".join([" " if x == 0 else "X" for x in line]))

def ans_1(D, max_x, max_y, times):
    ans = 0

    robots = [parse_robots(line) for line in D]

    for _ in range(times):
        for robot in robots:
            robot.x = (robot.x + robot.vol_x) % max_x
            robot.y = (robot.y + robot.vol_y) % max_y
    
    top_left = [robot for robot in robots if robot.x < max_x//2 and robot.y < max_y//2]
    top_right = [robot for robot in robots if robot.x > max_x//2 and robot.y < max_y//2]
    bottom_left = [robot for robot in robots if robot.x < max_x//2 and robot.y > max_y//2]
    bottom_right = [robot for robot in robots if robot.x > max_x//2 and robot.y > max_y//2]

    ans = len(top_left) * len(top_right) * len(bottom_right) * len(bottom_left)
    
    return ans

print(f"Ans 1 test: {ans_1(read_input(fp_0), 11, 7, 100)}")
print(f"Ans 0 real: {ans_1(read_input(fp_1), 101, 103, 100)}\n")

def ans_2(D, max_x, max_y, times):
    ans = 0
    
    robots = [parse_robots(line) for line in D]

    for x in range(times):
        at_pos = set()
        for robot in robots:
            robot.x = (robot.x + robot.vol_x) % max_x
            robot.y = (robot.y + robot.vol_y) % max_y
            at_pos.add((robot.x, robot.y))

        if len(at_pos) == len(robots):
            print_robots(robots)
        assert len(at_pos) != len(robots), x # Find out how many seconds needed
        
    
    #print_robots(0)
    
    return ans


#print(f"Ans 2 test: {ans_2(read_input(fp_0))}")
print(f"Ans 2 real: {ans_2(read_input(fp_1), 101, 103, 6446)}")
