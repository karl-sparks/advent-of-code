"""AOC day 14"""


print("AOC day 14")
fp_0 = "data/test-14.txt"
fp_1 = "data/day-14.txt"

def read_input(input):
    with open(input, encoding="utf-8") as f:
        D = [x.strip() for x in f.readlines()]

    return D

def ans_1(D):
    ans = 0

    print(D)
    
    return ans

print(f"Ans 1 test: {ans_1(read_input(fp_0))}")
#print(f"Ans 1 real: {ans_1(read_input(fp_1))}\n")

def ans_2(D):
    ans = 0
    
    return ans


#print(f"Ans 2 test: {ans_2(read_input(fp_0))}")
#print(f"Ans 2 real: {ans_2(read_input(fp_1))}")