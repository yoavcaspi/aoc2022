from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def func(val1, o, b):
    if b.isnumeric():
        val2 = int(b)
    else:
        assert b == "old"
        val2 = val1
    if o == "+":
        return val1 + val2
    elif o == "*":
        return val1 * val2
    else:
        assert False

class Monkey:
    def __init__(self):
        self.inspections = 0
        self.items = []
        self.op = None
        self.test_num = None
        self.throw_to_true = None
        self.throw_to_false = None


def compute(s: str) -> int:
    board = defaultdict(int)
    S = None
    E = None
    for y, line in enumerate(s.strip().splitlines()):
        for x, c in enumerate(line):
            if c == "S":
                board[x,y] = 1
                S = x, y
            elif c == "E":
                board[x,y] = 26
                E = x, y
            else:
                assert c.islower()
                board[x,y] = ord(c) - ord("a") + 1
    print(len(board))
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    q = [(E, 0)]
    visited = {E}
    while q:
        q.sort(key=lambda x: x[1])
        (x, y), m = q.pop(0)
        print(board[x,y], x, y)
        for (x1, y1) in moves:
            new_x = x + x1
            new_y = y + y1
            if (new_x, new_y) in visited:
                continue
            if board[new_x, new_y] > 0 and (board[x,y] - board[new_x, new_y]  <= 1):
                if board[new_x,new_y] == 1:
                    return m + 1
                visited.add((new_x, new_y))
                q.append(((new_x,new_y), m + 1))

    print(len(visited))
    return -1


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
