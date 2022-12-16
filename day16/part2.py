from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x, y, bx, by):
    return abs(bx - x) + abs(by - y)


class Valve:
    def __init__(self, name, rate, ns):
        self.name = name
        self.rate = rate
        self.ns = {n: 1 for n in ns}


visited = {}
jjj = 0

def find_best_sol(minutes, node, g, cur, o, valid_valves, prev = None):
    if (minutes, node, o) in visited:
        return visited[(minutes, node, o)]
    if minutes == 0 or o == valid_valves:
        return cur
    max_val = cur
    if node not in o and g[node].rate > 0:
        o2 = frozenset(o ^ {node})
        max_val = max(max_val, g[node].rate * (minutes - 1) + find_best_sol(minutes-1, node, g, cur, o2, valid_valves))
    for n in g[node].ns:
        if prev is not None and prev == n:
            continue
        max_val = max(max_val, find_best_sol(minutes-1, n, g, cur, o, valid_valves, node))
    visited[minutes, node, o] = max_val

    return max_val


def find_best_sol2(m_a, node_a, m_b, node_b, g, cur, o, valid_valves, first = None):
    if (m_a, node_a, m_b, node_b, o) in visited:
        return visited[(m_a, node_a, m_b, node_b, o)]
    if o == valid_valves:
        return cur
    max_val = cur
    for n in valid_valves - o:
        if first:
            print(o, max_val)
        size = g[node_a].ns[n]
        if m_a > size:
            o2 = frozenset(o ^ {n})
            max_val = max(max_val, find_best_sol2(m_a - size - 1, n, m_b, node_b, g, cur + (g[n].rate * (m_a - size - 1)), o2, valid_valves))
    for n in valid_valves - o:
        if first:
            print(o, max_val)
        size = g[node_b].ns[n]
        if m_b > size:
            o2 = frozenset(o ^ {n})
            max_val = max(max_val, find_best_sol2(m_a, node_a, m_b - size - 1, n, g, cur + (g[n].rate * (m_b - size - 1)), o2, valid_valves))
    visited[m_a, node_a, m_b, node_b, o] = max_val
    visited[m_b, node_b, m_a, node_a, o] = max_val

    return max_val


def compute(s: str) -> int:
    g = {}
    print()
    for line in s.strip().splitlines():
        vals = line.split()
        name = vals[1]
        rate = int(vals[4][5:-1])
        if "valves" in line:
            ns = line.split(" valves ")[1].split(", ")
        else:
            ns = line.split(" valve ")[1].split(", ")
        print(rate, ns)
        g[name] = Valve(name, rate, ns)

    # Remove unnecessary nodes
    remove_nodes = set()
    for name, val in g.items():
        if name == "AA":
            continue
        elif len(val.ns) == 2 and val.rate == 0:
            # Just a tunnel
            remove_nodes.add(name)
            n1, n2 = val.ns.keys()

            val1 = g[n1].ns.pop(name)
            val2 = g[n2].ns.pop(name)
            g[n1].ns[n2] = val1 + val2
            g[n2].ns[n1] = val1 + val2
    for name in remove_nodes:
        g.pop(name)
    for name1, val1 in g.items():
        q = deque([(name1, 0)])
        v = {name1}
        while q:
            node, val = q.popleft()
            for n, val2 in g[node].ns.items():
                if n in v:
                    continue
                q.append((n, val + val2))
                v.add(n)
                min_dist = g[name1].ns.get(n, 26)
                g[name1].ns[n] = min(min_dist, val + val2)
    for name1, val1 in g.items():
        for name2, val2 in g.items():
            if name1 == name2:
                continue
            val1.ns[name2] = min(val1.ns[name2], val2.ns[name1])

    valid_valves = set([k for k, v in g.items() if v.rate > 0])
    res = find_best_sol2(26, "AA", 26, "AA", g, 0, frozenset(), valid_valves, True)
    return res


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1707


# @pytest.mark.parametrize(
#     ('input_s', 'expected'),
#     (
#         (INPUT_S, EXPECTED),
#     ),
# )
# def test(input_s: str, expected: int) -> None:
#     assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
