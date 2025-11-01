from collections import deque

wires = {}

class Gate:
    def __init__(self, type_: str, inputs: list[str], output: str):
        self.type_ = type_
        self.inputs = inputs
        self.output = output

    def apply(self):
        if self.inputs[0] in wires and self.inputs[1] in wires:
            match self.type_:
                case "AND":
                    wires[self.output] = wires[self.inputs[0]] & wires[self.inputs[1]]
                case "OR":
                    wires[self.output] = wires[self.inputs[0]] | wires[self.inputs[1]]
                case "XOR":
                    wires[self.output] = wires[self.inputs[0]] ^ wires[self.inputs[1]]
                case _:
                    raise ValueError(f"Unknown gate type: {self.type_}")
            return True
        return False

def get_wire_value(type_of_wire: str) -> int:
    ans = 0
    for wire, value in wires.items():
        if type_of_wire in wire:
            sig = int(wire[1:])
            add_ans = 10**(sig * int(value)) if value else 0
            ans += add_ans
    return str(ans)

def parse_input(data: str):
    initial_wire_state, gates_input = data.split("\n\n")

    gates = []

    for line in gates_input.splitlines():
        input_1, gate_type, input_2, _, output = line.split()
        gate = Gate(gate_type, [input_1, input_2], output)
        gates.append(gate)

    for line in initial_wire_state.splitlines():
        wire, value = line.split(": ")
        wires[wire] = int(value)

    x_v = get_wire_value("x")
    y_v = get_wire_value("y")
    print(x_v)
    print(y_v)

    print(str(bin(int(x_v, 2) + int(y_v, 2)))[2:])

    return gates

def part_one(gates) -> int:
    print("Running part one")
    sim_que = deque(gates)
    while sim_que:
        next_gate = sim_que.popleft()
        if not next_gate.apply():
            sim_que.append(next_gate)

    print("Part one complete")

    ans = get_wire_value("z")

    print(ans)
    
    return int(ans, 2)

if __name__ == "__main__":
    print("AOC day 24")
    with open(0, encoding="utf-8") as f:
        D = f.read()

    gates = parse_input(D)
    
    print(f"Part 1 Ans: {part_one(gates)}")