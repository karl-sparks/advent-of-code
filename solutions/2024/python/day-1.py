"""AOC day 1"""

print("AOC day 1")
with open("data/test.txt", encoding="utf-8") as f:
    D = f.read()

list_1 = []
list_2 = []
counts = {}
for lin in D.splitlines():
    n, x = lin.split("   ")
    list_1.append(int(n))
    list_2.append(int(x))
    num = int(x)
    if num in counts:
        counts[num] += 1
    else:
        counts[num] = 1
    
    
list_1.sort()
list_2.sort()    

ans = 0
for i in range(len(list_1)):
    diff = abs(list_1[i] - list_2[i])
    assert diff >= 0, f"Diff {diff} is negative for {i}, {list_1[i]}, {list_2[i]}"
    ans += diff

print(f"Ans: {ans}")


ans_2 = 0
for first_num in list_1:
    if first_num in counts:
        ans_2 += first_num * counts[first_num]

print(f"Ans part 2: {ans_2}")