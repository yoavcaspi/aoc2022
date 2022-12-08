from __future__ import annotations

from collections import deque, Counter, defaultdict
import argparse
import os.path
from dataclasses import dataclass
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def calc_score(board, x1, y1, max_x, max_y):
    h = board[x1,y1]
    res = 1
    c = 0
    for x in reversed(range(x1)):
        c += 1
        if board[x, y1] >= h:
            break
    res*=c

    c = 0
    for x in range(x1+1, max_x):
        c+=1
        if board[x,y1] >= h:
            break
    res*=c


    c = 0
    for y in reversed(range(y1)):
        c+=1
        if board[x1, y] >= h:
            break
    res*=c

    c = 0
    for y in range(y1+1, max_y):
        c+=1
        if board[x1, y] >= h:
            break
    res *= c

    return res

def compute(s: str) -> int:
    board = defaultdict(int)
    max_y = len(s.split("\n")) - 1
    max_x = len(s.split("\n")[0])
    print(max_x, max_y)
    for (y, line) in enumerate(s.strip().splitlines()):
        for x, d in enumerate(line):
            board[x,y] = int(d)

    assert max_x == max_y
    max_score = 0
    for y in range(max_y):
        for x in range(max_x):
            score = calc_score(board, x, y, max_x, max_y)
            max_score = max(max_score, score)
    return max_score


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
EXPECTED = 8


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
