from __future__ import annotations

from collections import deque, Counter, defaultdict
import argparse
import os.path
from dataclasses import dataclass
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Directory:
    def __init__(self, name):
        self.name = name
        self.dirs = {}
        self.size = 0
        self.files = []
        self.parent = None

    def add_file(self, size):
        self.size += size
        if self.parent:
            self.parent.add_file(size)

    def add_dir(self, name):
        d = Directory(name)
        d.parent = self
        self.dirs[name] = d


def is_visible(board, x1, y1, max_x, max_y):
    h = board[x1,y1]
    for x in range(x1):
        if board[x,y1] >= h:
            break
    else:
        return True

    for x in range(x1+1, max_x):
        if board[x,y1] >= h:
            break
    else:
        return True

    for y in range(y1):
        if board[x1,y] >= h:
            break
    else:
        return True

    for y in range(y1+1, max_y):
        if board[x1,y] >= h:
            break
    else:
        return True

    return False

def compute(s: str) -> int:
    board = defaultdict(int)
    max_y = len(s.split("\n")) - 1
    max_x = len(s.split("\n")[0])
    print(max_x, max_y)
    for (y, line) in enumerate(s.strip().splitlines()):
        for x, d in enumerate(line):
            board[x,y] = int(d)

    assert max_x == max_y
    res = 0
    for y in range(max_y):
        for x in range(max_x):
            if is_visible(board, x, y, max_x, max_y):
                res+=1
    print_board(board, max_x, max_y)
    return res
#1552 - Too Low
#1651 - too low

def print_board(board, max_x, max_y):
    for y in range(max_y):
        for x in range(max_x):
            print(board[x, y], end=" ")
        print()


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
