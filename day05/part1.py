from __future__ import annotations

import re
from collections import deque
import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    board_raw, moves = s.split("\n\n")
    board_raw = board_raw.split("\n")
    rows = len(board_raw[0]) // 4 + 1
    print(rows)
    board = [deque() for i in range(rows)]

    for line in board_raw[:-1]:
        for i in range(0, rows):

            start = i + i*3
            val = line[start:start+3]
            if val != "   ":
                board[i].append(val[1])
    print(board)
    for line in moves.strip().split("\n"):
        pattern = re.match("move (\d+) from (\d) to (\d)", line)
        count = int(pattern.groups()[0])
        f = int(pattern.groups()[1]) - 1
        t = int(pattern.groups()[2]) - 1
        for _ in range(count):
            crate = board[f].popleft()
            board[t].appendleft(crate)
    res = ""
    for i in range(rows):
        c = board[i].popleft()
        res+=c
    return res


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = "CMZ"


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
