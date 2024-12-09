"""AOC day 9"""

from collections import defaultdict
from itertools import combinations
import math

print("AOC day 8")
fp_0 = "data/test.txt"
fp_1 = "data/day-9.txt"

with open(fp_1, encoding="utf-8") as f:
    D = [x.strip() for x in f.readlines()]
    
assert len(D)
total_n = len(D[0])
free_space_id = total_n + 1

print(f"Input length: {total_n}\n")

def gen_long_mem(D):
    free_space = False
    new_seq = ""
    m_id = 0
    for c in D[0]:
        if free_space:
            new_seq += chr(free_space_id) * int(c)
            free_space = False
        else:
            new_seq += chr(m_id) * int(c)
            free_space = True
            m_id += 1
        
    return [x for x in new_seq]

def sort_long_mem(long_seq):
    for i in reversed(range(len(long_seq))):
        if i % 10000 == 0:
            print(f"At character {i} out of {len(long_seq)}")
        if long_seq[i] != chr(free_space_id):
            for s in range(len(long_seq)):
                if s >= i:
                    break
                elif long_seq[s] == chr(free_space_id):
                    long_seq[s] = long_seq[i]
                    long_seq[i] = chr(free_space_id)
                    break 
    return long_seq

def ans_1(D):
    ans = 0
    
    exp_seq = gen_long_mem(D)
        
    sorted_seq = sort_long_mem(exp_seq)

    for i, c in enumerate(sorted_seq):
        if ord(c) != free_space_id:
            ans += i * ord(c)
        
    return ans

print(f"Ans 1: {ans_1(D)}")

def sort_long_mem_block(long_seq):
    failed_sort_ids = set()
    
    for i in reversed(range(len(long_seq))):
        if i % 10000 == 0:
            print(f"At character {i} out of {len(long_seq)}")
        if long_seq[i] != chr(free_space_id) and long_seq[i] not in failed_sort_ids:
            m_id = long_seq[i]
            left_id = i
            while long_seq[left_id] == m_id:
                left_id -= 1
                
            left_id += 1

            length = i - left_id + 1

            for s in range(len(long_seq)):
                if s + length >= i:
                    break
                elif long_seq[s] == chr(free_space_id):
                    right_id = s
                    
                    if length > 1:
                        while long_seq[right_id] == chr(free_space_id) and right_id - s < length:
                            right_id += 1
                        
                        if right_id - s < length:
                            continue
                    
                        assert right_id - s == length,  f"{i} : {right_id} : {s} : {length} : {[ord(x) if ord(x) != free_space_id else "." for x in long_seq]}"
                    
                    for n in range(length):
                        assert long_seq[s + n] == chr(free_space_id), f"{i} : {s} : {n}: {[ord(x) if ord(x) != free_space_id else "." for x in long_seq]}"
                        assert ord(long_seq[i - n]) != free_space_id
                        long_seq[s + n] = long_seq[i - n]
                        long_seq[i - n] = chr(free_space_id)
                    break 
            failed_sort_ids.add(m_id)
            
    return long_seq

print(" "* 100)

def ans_2(D):
    ans = 0
    exp_seq = gen_long_mem(D)
    
    sorted_seq = sort_long_mem_block(exp_seq)
    
    for i, c in enumerate(sorted_seq):
        if ord(c) != free_space_id:
            ans += i * ord(c)
    
    return ans

print(f"Ans 2: {ans_2(D)}")