from collections import deque


def get_wire_value(wire_states: dict[str, int], type_of_wire: str) -> str:
    ans_wires = [wire for wire in wire_states if type_of_wire in wire]

    ans_wires.sort(reverse=True)

    ans = ""

    for wire in ans_wires:
        ans += str(wire_states[wire])

    return ans


def parse_input(
    data: str,
) -> tuple[dict[str, str], dict[str, tuple[str, str]], dict[str, int]]:
    initial_wire_state, gates_input = data.split("\n\n")

    gate_type: dict[str, str] = {}
    gate_inputs: dict[str, tuple[str, str]] = {}
    wire_state: dict[str, int] = {}

    for line in gates_input.splitlines():
        input_1, type, input_2, _, output = line.split()
        gate_type[output] = type
        gate_inputs[output] = (input_1, input_2)

    for line in initial_wire_state.splitlines():
        wire_id, value = line.split(": ")
        wire_state[wire_id] = int(value)

    return gate_type, gate_inputs, wire_state


def apply_gate(
    gate: str,
    gate_type: dict[str, str],
    gate_inputs: dict[str, tuple[str, str]],
    wire_state: dict[str, int],
) -> bool:
    input_1, input_2 = gate_inputs[gate]
    if input_1 in wire_state and input_2 in wire_state:
        match gate_type[gate]:
            case "AND":
                wire_state[gate] = wire_state[input_1] & wire_state[input_2]
            case "OR":
                wire_state[gate] = wire_state[input_1] | wire_state[input_2]
            case "XOR":
                wire_state[gate] = wire_state[input_1] ^ wire_state[input_2]
            case _:
                raise ValueError(f"Unknown gate type: {gate_type}")
        return True
    return False


def calc_gates(
    gate_type: dict[str, str],
    gate_inputs: dict[str, tuple[str, str]],
    wire_state: dict[str, int],
) -> None:
    sim_que = deque(list(gate_inputs.keys()))
    while sim_que:
        next_gate = sim_que.popleft()
        if not apply_gate(next_gate, gate_type, gate_inputs, wire_state):
            sim_que.append(next_gate)

    return None


def get_deps(gate: str, gate_inputs: dict[str, tuple[str, str]]) -> set[str]:
    deps = set([gate])
    if gate not in gate_inputs:
        return deps

    for input in gate_inputs[gate]:
        deps.update(get_deps(input, gate_inputs))

    return deps


def part_one(D: str) -> int:
    print("Running part one")
    gate_type, gate_inputs, wire_state = parse_input(D)

    calc_gates(gate_type, gate_inputs, wire_state)

    ans = get_wire_value(wire_state, "z")

    return int(ans, 2)


def part_two(D: str) -> int:
    print("Running part two")
    gate_type, gate_inputs, wire_state = parse_input(D)
    x_v = get_wire_value(wire_state, "x")
    y_v = get_wire_value(wire_state, "y")

    true_ans = str(bin(int(x_v, 2) + int(y_v, 2)))[2:]

    calc_gates(gate_type, gate_inputs, wire_state)

    ans = get_wire_value(wire_state, "z")

    ans_diff = str(bin(int(true_ans, 2) ^ int(ans, 2)))[2:]
    print(true_ans)
    print(str(ans).zfill(len(true_ans)))
    print(str(ans_diff).zfill(len(true_ans)))
    print(list(reversed(ans_diff)))

    deps_1 = get_deps("z01", gate_inputs)
    deps_2 = get_deps("z02", gate_inputs)
    print(deps_1)
    print(deps_2)

    return int(ans, 2)


if __name__ == "__main__":
    print("AOC day 24\n")
    with open(0, encoding="utf-8") as f:
        D = f.read()

    print(f"Part 1 Ans: {part_one(D)}\n")
    print(f"Part 2 Ans: {part_two(D)}")
