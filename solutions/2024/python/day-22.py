def mix(s_num, num_to_mix_in) -> int:
    return s_num ^ num_to_mix_in

def prune(s_num) -> int:
    return s_num % 16777216


def step_one(s_num: int) -> int:
    return prune(mix(s_num, s_num*64))

def step_two(s_num: int) -> int:
    return prune(mix(s_num, s_num // 32))

def step_three(s_num: int) -> int:
    return prune(mix(s_num, s_num*2048))

def step_s_num(s_num: int) -> int:
    s_num = step_one(s_num)
    s_num = step_two(s_num)
    s_num = step_three(s_num)
    return s_num

def get_price(s_num: int) -> int:
    return s_num % 10

def get_secret_numbers(line: str) -> list[int]:
    s_num = int(line)
    secret_numbers = [s_num]

    for _ in range(2000):
        s_num = step_s_num(s_num)
        secret_numbers.append(s_num)
    
    return secret_numbers
    

def part_one(monkeys) -> int:
    total = 0
    for monkey in monkeys:
        total += monkey[-1]

    return total

def part_two(monkeys) -> int:
    changes = []
    for monkey in monkeys:
        change = []
        for i in range(1, len(monkey)):
            change.append(get_price(monkey[i]) - get_price(monkey[i-1]))
        changes.append(change)

    prices = []
    all_signs = set()
    for m, change in enumerate(changes):
        signs = {}
        for i in range(3, len(change)):
            sign = (change[i-3], change[i-2], change[i-1], change[i])
            if sign not in signs:
                signs[sign] = get_price(monkeys[m][i+1])
            all_signs.add(sign)
        prices.append(signs)

    max_profit = 0
    max_profit_sign = None
    for sign in all_signs:
        profit = 0
        for i in prices:
            if sign in i:
                profit += i[sign]
        if profit > max_profit:
            max_profit = profit
            max_profit_sign = sign

    print("Max profit sign:", max_profit_sign)
    return max_profit

if __name__ == "__main__":
    print("AOC day 22")
    with open(0, encoding="utf-8") as f:
        D = f.read()

    monkeys = []
    for line in D.splitlines():
        monkeys.append(get_secret_numbers(line))
    
    print("Answer part one: ", part_one(monkeys))

    print("Answer part two: ", part_two(monkeys))
