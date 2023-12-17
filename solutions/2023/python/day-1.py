"""AOC day 1"""

with open(0, encoding="utf-8") as f:
    D = f.read()


def get_number_p1(input_str: str):
    digits = []
    for ch in input_str:
        if ch.isdigit():
            digits.append(ch)

    result = ""

    if digits:
        result = digits[0] + digits[-1]

    return int(result) if result else 0


digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_number_p2(input_str: str):
    digits = []
    for i, ch in enumerate(input_str):
        for check_digit, append_digit in digit_map.items():
            if input_str[i:].startswith(check_digit):
                digits.append(append_digit)

        if ch.isdigit():
            digits.append(ch)

    result = ""

    if digits:
        result = digits[0] + digits[-1]

    return int(result) if result else 0


ans_1 = 0
ans_2 = 0
for line in D.splitlines():
    ans_1 += get_number_p1(line)
    ans_2 += get_number_p2(line)

print("P1: ", ans_1)
print("P2: ", ans_2)
