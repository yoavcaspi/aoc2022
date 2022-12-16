from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x, y, bx, by):
    return abs(bx - x) + abs(by - y)


class Valve:
    def __init__(self, name, rate, ns):
        self.name = name
        self.rate = rate
        self.ns = ns


visited = {}


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
        max_val = max(max_val, find_best_sol(minutes-1, n, g, cur, o, valid_valves, node))
    visited[minutes, node, o] = max_val

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
    valid_valves = set([k for k, v in g.items() if v.rate > 0])
    return find_best_sol(30, "AA", g, 0, frozenset(), valid_valves)


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
EXPECTED = 1651


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
