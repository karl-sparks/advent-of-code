from collections import deque

with open(0, encoding="utf-8") as f:
    D = f.read()

grid = [[x for x in row] for row in D.splitlines()]

R, C = len(grid), len(grid[0])

start, end = (0, 1), (R - 1, C - 2)

dirs = {"E": (0, 1), "W": (0, -1), "S": (1, 0), "N": (-1, 0)}


class node:
    def __init__(self, pos, next_nodes):
        self.pos = pos
        self.connected = next_nodes


def get_connections(pos, path):
    path.add(pos)

    r, c = pos

    new_steps = []

    for d in "EWSN":
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc

        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and (nr, nc) not in path:
            new_steps.append((nr, nc))

    if len(new_steps) == 1:
        return get_connections(new_steps[0], path)
    else:
        return pos, len(path) - 1, new_steps


start_node = node(pos=start, next_nodes={})

que = deque([(start_node, start)])
seen = set([start])
nodes = {}

while que:
    old_node, new_pos = que.popleft()

    pos, steps, new_steps = get_connections(new_pos, set([old_node.pos]))

    if pos in nodes:
        new_node = nodes[pos]
    else:
        new_node = node(pos, {old_node.pos: steps})

    nodes[pos] = new_node

    old_node.connected[new_node.pos] = steps
    new_node.connected[old_node.pos] = steps

    for n in new_steps:
        if n not in seen:
            que.append((new_node, n))
            seen.add(n)

que = deque([(0, start_node, [])])

max_l_nodes = {start: 0}

while que:
    cur_steps, next_node, cur_path = que.popleft()
    cur_path.append(next_node.pos)
    for k, v in next_node.connected.items():
        if k in cur_path:
            continue

        if k not in max_l_nodes:
            max_l_nodes[k] = v + cur_steps
        else:
            max_l_nodes[k] = max(max_l_nodes[k], v + cur_steps)

        que.append((v + cur_steps, nodes[k], cur_path.copy()))


print("part 2:", max_l_nodes[end])
