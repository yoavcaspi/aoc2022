from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


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
    q = [(S, 0)]
    visited = {S}
    while q:

        (x, y), m = q.pop(0)
        print(board[x,y], x, y)
        for (x1, y1) in moves:
            new_x = x + x1
            new_y = y + y1
            if (new_x, new_y) in visited:
                continue
            if board[new_x, new_y] > 0 and (board[new_x, new_y] - board[x,y] <= 1):
                if E == (new_x, new_y):
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
EXPECTED = 31


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
