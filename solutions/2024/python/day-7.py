"""AOC day 7"""

print("AOC day 7")
fp_0 = "data/test.txt"
fp_1 = "data/day-7.txt"

with open(fp_1, encoding="utf-8") as f:
    D = [x.strip() for x in f.readlines()]


def calc_options(curr, rem_nums):
    if not rem_nums:
        return {curr}
    
    return_set = set()
    
    return_set.update(calc_options(curr + rem_nums[0], rem_nums[1:]))
    return_set.update(calc_options(curr * rem_nums[0], rem_nums[1:]))
    return_set.update(calc_options(int(str(curr) + str(rem_nums[0])), rem_nums[1:]))
    
    return return_set

def ans_1(D):
    ans = 0
    
    for line in D:
        t_value, nums = line.split(": ")
        t_value = int(t_value)
        nums = [int(x) for x in nums.split(" ")]

        pos_values = calc_options(nums[0], nums[1:])

        if t_value in pos_values:
            ans += t_value
    
    return ans

print(f"Ans 1: {ans_1(D)}")