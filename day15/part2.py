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


def compute(s: str, max_val = 4000000) -> int:
    board = set()
    sensors = []
    min_x = 0
    max_x = 0
    print()
    for line in s.strip().splitlines():
        match = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        x, y, bx, by = [int(val) for val in match.groups()]
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        board.add((x,y))
        board.add((bx, by))
        sensors.append(Sensor(x,y,bx,by))
    val_count = 4000000
    for sensor in sensors:
        print(sensor)
        x, y = sensor.x, sensor.y
        d = sensor.dist
        # Top right
        y2 = y + d + 1
        x2 = x
        for i in range(d+1):
            x3 = x2 - i
            y3 = y2 - i
            if x3 < 0 or x3 > max_val or y3 < 0 or y3 > max_val:
                continue
            if (x3, y3) in board:
                continue
            for sensor in sensors:
                if dist(x3, y3, sensor.x, sensor.y) <= sensor.dist:
                    break
            else:
                return (x3) * val_count + (y3)

    return -1
# 1573496696899 - too low
#   11318723411840
# 11318723411840
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
EXPECTED = 56000011


# @pytest.mark.parametrize(
#     ('input_s', 'expected'),
#     (
#         (INPUT_S, EXPECTED),
#     ),
# )
# def test(input_s: str, expected: int) -> None:
#     assert compute(input_s, 20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
