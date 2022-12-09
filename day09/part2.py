from __future__ import annotations

from collections import deque, Counter, defaultdict
import argparse
import os.path
from dataclasses import dataclass
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(t, h):
    x1, y1 = t
    x2, y2 = h
    return abs(x1-x2) + abs(y1-y2)


def move(t, h):
    x1, y1 = t
    x2, y2 = h
    x = (max(x1, x2) + min(x1, x2)) // 2
    y = (max(y1, y2) + min(y1, y2)) // 2
    if abs(x2-x1) == 2 and abs(y2-y1) == 2:
        return x, y
    elif abs(x2-x1) == 2:
        return x, y2
    elif abs(y2-y1) == 2:
        return x2, y
    else:
        return x1, y1



def compute(s: str) -> int:
    r = [(0,0)] * 10
    visited = set()
    for line in s.strip().splitlines():
        d, c = line.split()
        for _ in range(int(c)):
            x, y = r[0]
            if d == "R":
                r[0] = x + 1, y
            elif d == "L":
                r[0] = x - 1, y
            elif d == "U":
                r[0] = x, y + 1
            elif d == "D":
                r[0] = x, y - 1
            else:
                assert False, line
            for i in range(len(r) - 1):
                if dist(r[i + 1], r[i]) >= 2:
                    r[i+1] = move(r[i + 1], r[i])
            visited.add(r[-1])

    visited.add(r[-1])
    return len(visited)



INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
