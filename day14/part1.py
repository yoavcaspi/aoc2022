from __future__ import annotations

import argparse
import ast
import os.path
from collections import defaultdict
from itertools import zip_longest

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    board = defaultdict(lambda: ".")
    max_y = 0
    for line in s.strip().splitlines():
        points = line.split(" -> ")
        x1, y1 = [int(p) for p in points[0].split(",")]
        max_y = max(max_y, y1)
        for p2 in points[1:]:
            x2, y2 = [int(t) for t in p2.split(",")]
            max_y = max(max_y, y2)
            if x1 == x2:
                for y in range(min(y1,y2), max(y1,y2) + 1):
                    board[x1,y] = "#"
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    board[x, y1] = "#"
            else:
                assert False
            x1 = x2
            y1 = y2
    # print()
    # for y in range(10):
    #     for x in range(494, 504):
    #         print(board[x,y], end="")
    #     print()
    # print(max_y)
    i = 0
    while board[500,0] == ".":
        x,y = 500, 0
        while True:
            if y > max_y:
                board[x, y] = "O"
                break
            if board[x,y+1] == ".":
                y += 1
            elif board[x-1,y+1] == ".":
                y += 1
                x -= 1
            elif board[x+1, y+1] == ".":
                y += 1
                x += 1
            else:
                board[x, y] = "O"
                break
        i+=1
    return i


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
