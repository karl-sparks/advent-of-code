from collections import Counter

with open(0, encoding="utf-8") as f:
    D = f.read()


def detect_start_signal(line, min_len):
    chec = ""
    for i, c in enumerate(line):
        id_i = i + 1
        if len(chec) >= min_len:
            chec = chec[1:] + c
            assert len(chec) == min_len
            if all(x == 1 for x in Counter(chec).values()):
                return id_i
        else:
            chec += c


for line in D.splitlines():
    print("Part 1:", detect_start_signal(line, 4))
    print("Park 2:", detect_start_signal(line, 14))

# qmgbljsphdztnv
