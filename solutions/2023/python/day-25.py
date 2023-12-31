import heapq
import math
import random
from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import combinations

with open(0, encoding="utf-8") as f:
    D = f.read()

components_raw = [[v.split() for v in x.split(": ")] for x in D.splitlines()]


@dataclass
class node:
    name: str
    cons: dict = field(default_factory=dict)


components_map = {}
components = {}

for n, v in components_raw:
    assert len(n) == 1

    components[n[0]] = node(name=n)
    components_map[n[0]] = v

keys = list(components.keys())
for n in keys:
    for link in components_map[n]:
        if link not in components:
            link_node = node(name=link)
            components[link] = link_node
        else:
            link_node = components[link]

        components[n].cons[link] = link_node
        link_node.cons[n] = components[n]


def find_edgeness(components):
    edgeness = defaultdict(lambda: 0)

    all_combinations = list(combinations(components, 2))

    if len(all_combinations) > 1000:
        selected_combinations = random.sample(all_combinations, 1_000)
    else:
        selected_combinations = all_combinations

    num = 0
    end = len(selected_combinations)

    print(end, "possible combinations")

    for source, target in selected_combinations:
        if num % (end // 100) == 0:
            print(f"Edgeness: {num / end * 100:.0f}")
        num += 1

        que = [(0, source, set())]
        heapq.heapify(que)
        seen = set()

        while que:
            steps, curr_node, path = heapq.heappop(que)

            seen.add(curr_node)

            for link in components[curr_node].cons:
                if curr_node == target:
                    for nm in path:
                        edgeness[nm] += 1
                if link not in seen:
                    link_key = tuple(sorted((curr_node, link)))
                    assert link_key not in path
                    copy_path = path.copy()
                    copy_path.add(link_key)
                    heapq.heappush(que, (steps + 1, link, copy_path))

    return dict(edgeness)


print("Number of nodes: ", len(components))
print("Starting edgeness calculation")
edge = find_edgeness(components)
print("Found graph edgeness")

top_three = sorted(edge.items(), key=lambda item: item[1], reverse=True)[:3]

banned_links = [element for tuple_ in top_three for element in tuple_[0]]

print("Found cut links: ", banned_links)

first_cluster = set()
bfs_que = deque([banned_links[0]])

while bfs_que:
    next_node = bfs_que.pop()

    first_cluster.add(next_node)

    for link in components[next_node].cons:
        if link not in first_cluster and not (
            next_node in banned_links and link in banned_links
        ):
            bfs_que.appendleft(link)

print("Ans 1:", len(first_cluster) * (len(components) - len(first_cluster)))
