from collections import deque
from itertools import combinations


def get_wire_value(wire_states: dict[str, int], type_of_wire: str) -> str:
    ans_wires = [wire for wire in wire_states if type_of_wire in wire]

    ans_wires.sort(reverse=True)

    ans = ""

    for wire in ans_wires:
        ans += str(wire_states[wire])

    return ans


def parse_input(
    data: str,
) -> tuple[dict[str, tuple[str, str, str]], dict[str, int]]:
    initial_wire_state, gates_input = data.split("\n\n")

    gate_states: dict[str, tuple[str, str, str]] = {}
    wire_state: dict[str, int] = {}

    for line in gates_input.splitlines():
        input_1, type, input_2, _, output = line.split()
        gate_states[output] = (type, input_1, input_2)

    for line in initial_wire_state.splitlines():
        wire_id, value = line.split(": ")
        wire_state[wire_id] = int(value)

    return gate_states, wire_state


def apply_gate(
    gate: str,
    gate_states: dict[str, tuple[str, str, str]],
    wire_state: dict[str, int],
) -> bool:
    type, input_1, input_2 = gate_states[gate]
    if input_1 in wire_state and input_2 in wire_state:
        match type:
            case "AND":
                wire_state[gate] = wire_state[input_1] & wire_state[input_2]
            case "OR":
                wire_state[gate] = wire_state[input_1] | wire_state[input_2]
            case "XOR":
                wire_state[gate] = wire_state[input_1] ^ wire_state[input_2]
            case _:
                raise ValueError(f"Unknown gate type: {type}")
        return True
    return False


def calc_gates(
    gate_states: dict[str, tuple[str, str, str]],
    wire_state: dict[str, int],
) -> str:
    sim_que = deque(list(gate_states.keys()))
    while sim_que:
        next_gate = sim_que.popleft()
        if not apply_gate(next_gate, gate_states, wire_state):
            sim_que.append(next_gate)

    return get_wire_value(wire_state, "z")


def get_deps(gate: str, gate_states: dict[str, tuple[str, str, str]]) -> set[str]:
    deps: set[str] = set()
    if gate not in gate_states:
        return deps

    deps.add(gate)

    for input in gate_states[gate]:
        deps.update(get_deps(input, gate_states))

    return deps


def get_unique_deps(
    gate_states: dict[str, tuple[str, str, str]], z_bit: int
) -> set[str]:
    if z_bit == 0:
        return get_deps("z00", gate_states)
    return get_deps(f"z{z_bit:02}", gate_states) - get_deps(
        f"z{z_bit - 1:02}", gate_states
    )


def part_one(D: str) -> int:
    print("Running part one")
    gate_states, wire_state = parse_input(D)

    ans = calc_gates(gate_states, wire_state)

    return int(ans, 2)


def test_swaps(
    gates_to_test: set[str],
    gate_states: dict[str, tuple[str, str, str]],
    wire_state: dict[str, int],
    true_ans: str,
) -> tuple[str, str, str, str] | None:
    for x1, x2 in combinations(gates_to_test, 2):
        for y1, y2 in combinations(gates_to_test, 2):
            print(x1, x2, y1, y2)
            new_gate_states = gate_states.copy()
            (
                new_gate_states[x1],
                new_gate_states[x2],
                new_gate_states[y1],
                new_gate_states[y2],
            ) = (
                gate_states[x2],
                gate_states[x1],
                gate_states[y2],
                gate_states[y1],
            )
            ans = calc_gates(new_gate_states, wire_state.copy())
            if ans == true_ans:
                print(true_ans)
                print(str(ans).zfill(len(true_ans)))
                return (
                    x1,
                    x2,
                    y1,
                    y2,
                )
    print("Can't find a solution")
    return None


def create_fake_initial_wire_state(n: int, x_y: str, double: bool):
    other_x_y = "x" if x_y == "y" else "y"

    return {f"{x_y}{i:02}": 1 if i == n else 0 for i in range(45)} | {
        f"{other_x_y}{i:02}": 1 if i == n and double else 0 for i in range(45)
    }


def get_true_ans(wire_state: dict[str, int]) -> str:
    x_v = get_wire_value(wire_state, "x")
    y_v = get_wire_value(wire_state, "y")
    return str(bin(int(x_v, 2) + int(y_v, 2)))[2:]


def test_initial_wire_state(
    gate_states: dict[str, tuple[str, str, str]], i: int, x_y: str, double: bool
) -> set[int]:
    x_only = create_fake_initial_wire_state(i, x_y, double)

    ans_1 = calc_gates(gate_states, x_only)

    true_ans = get_true_ans(x_only)
    true_ans = str(true_ans).zfill(46)

    error_finals: set[int] = set()
    if ans_1 != true_ans:
        ans_l = len(ans_1)
        for t in range(ans_l):
            if ans_1[t] != true_ans[t]:
                error_finals.add(ans_l - t - 1)

    return error_finals


def validate_gates(gate_states: dict[str, tuple[str, str, str]]) -> set[int]:
    error_finals: set[int] = set()
    for i in range(45):
        error_finals |= test_initial_wire_state(gate_states, i, "x", False)
        error_finals |= test_initial_wire_state(gate_states, i, "y", False)
        error_finals |= test_initial_wire_state(gate_states, i, "x", True)

    return error_finals


def find_wire(
    gate_states: dict[str, tuple[str, str, str]],
    select_gate: str | None = None,
    select_type: str | None = None,
    select_input_1: str | None = None,
    select_input_2: str | None = None,
) -> str | None:
    for gate, (type, input_1, input_2) in gate_states.items():
        _inputs = [input_1, input_2]
        if select_gate and gate != select_gate:
            continue
        if select_type and type != select_type:
            continue
        if select_input_1 and select_input_1 not in _inputs:
            continue
        if select_input_2 and select_input_2 not in _inputs:
            continue
        return gate
    return None


def gate_struct(
    gate_states: dict[str, tuple[str, str, str]], z_bit: int
) -> set[str] | None:
    """
    g1  px  py AND
    g2  cx  cy XOR
    g3 pg2 pg4 AND
    g4  g1  g3 OR
    ot  g4  g2 XOR
    """
    g1 = find_wire(
        gate_states,
        select_type="AND",
        select_input_1=f"x{z_bit - 1:02}",
        select_input_2=f"y{z_bit - 1:02}",
    )

    g2 = find_wire(
        gate_states,
        select_type="XOR",
        select_input_1=f"x{z_bit:02}",
        select_input_2=f"y{z_bit:02}",
    )

    pg2 = find_wire(
        gate_states,
        select_type="XOR",
        select_input_1=f"x{z_bit - 1:02}",
        select_input_2=f"y{z_bit - 1:02}",
    )

    g3 = find_wire(gate_states, select_type="AND", select_input_1=pg2)

    g4 = find_wire(
        gate_states,
        select_type="OR",
        select_input_1=g1,
        select_input_2=g3,
    )

    ot = find_wire(
        gate_states,
        select_type="XOR",
        select_input_1=g4,
        select_input_2=g2,
    )

    currect_ot = f"z{z_bit:02}"

    if ot is None:
        ot = currect_ot
        _, in_1, in_2 = gate_states[ot]

        return set([in_1, in_2]) ^ set([g4, g2])
    if ot != currect_ot:
        return set([ot, currect_ot])

    return None


def apply_swap(
    gate_states: dict[str, tuple[str, str, str]], gate_1: str, gate_2: str
) -> None:
    gate_states[gate_1], gate_states[gate_2] = gate_states[gate_2], gate_states[gate_1]


def part_two(D: str) -> str:
    print("Running part two")
    initial_gate_states, _ = parse_input(D)

    error_gates = validate_gates(initial_gate_states)

    curr_gates = initial_gate_states.copy()

    sol_q = deque(list(error_gates))

    ans: set[str] = set()

    while sol_q:
        e_gate = sol_q.popleft()
        print(f"trying to correct z{e_gate:02}")
        swap_gates = gate_struct(gate_states=curr_gates, z_bit=e_gate)
        print(f"Found swaps {swap_gates}")
        if swap_gates:
            print(f"Applying swaps: {swap_gates}")
            ans.update(swap_gates)
            apply_swap(curr_gates, *swap_gates)
            sol_q = deque(list(validate_gates(curr_gates)))
            print(f"New error gates: {list(sol_q)}")

    return ",".join(sorted(list(ans)))


if __name__ == "__main__":
    print("AOC day 24\n")
    with open(0, encoding="utf-8") as f:
        D = f.read()

    print(f"Part 1 Ans: {part_one(D)}\n")
    print(f"Part 2 Ans: {part_two(D)}")
