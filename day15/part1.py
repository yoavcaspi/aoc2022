from __future__ import annotations

import argparse
import ast
import os.path
import re
from collections import defaultdict
from itertools import zip_longest

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x, y, bx, by):
    return abs(bx - x) + abs(by - y)


class Sensor:
    def __init__(self, x, y, bx, by):
        self.x = x
        self.y = y
        self.dist = dist(x,y,bx,by)


def compute(s: str, row = 2000000) -> int:
    board = set()
    sensors = []
    print()
    min_x = 0
    max_x = 0
    for line in s.strip().splitlines():
        match = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        x, y, bx, by = [int(val) for val in match.groups()]
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        if y == row:
            board.add(x)
        elif by == row:
            board.add(bx)
        sensors.append(Sensor(x,y,bx,by))
    max_dist = max([sensor.dist for sensor in sensors])
    count = 0
    i = 0
    for val in range(min_x - max_dist, max_x + max_dist +1):
        i+=1
        if i % 50000 == 0:
            print(val)
        for sensor in sensors:
            if dist(val, row, sensor.x, sensor.y) <= sensor.dist and val not in board:
                break
        else:
            continue
        count += 1
    return count


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


# @pytest.mark.parametrize(
#     ('input_s', 'expected'),
#     (
#         (INPUT_S, EXPECTED),
#     ),
# )
# def test(input_s: str, expected: int) -> None:
#     assert compute(input_s, 10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
