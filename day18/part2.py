from __future__ import annotations

import argparse
import os.path
from collections import defaultdict, deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    cubes = {}
    for line in s.strip().splitlines():
        x, y, z = [int(val) for val in line.split(",")]
        sides = 6
        for x2, y2, z2 in cubes.keys():
            if abs(x-x2) + abs(y-y2) + abs(z-z2) == 1:
                sides -= 1
                cubes[x2,y2,z2] -= 1
        cubes[(x,y,z)] = sides

    min_x = min([x for x, y, z in cubes]) - 1
    max_x = max([x for x, y, z in cubes]) + 2
    min_y = min([y for x, y, z in cubes]) - 1
    max_y = max([y for x, y, z in cubes]) + 2
    min_z = min([z for x, y, z in cubes]) - 1
    max_z = max([z for x, y, z in cubes]) + 2
    q = deque([(min_x,min_y,min_z)])
    visited = set()
    c = 0
    print()
    while q:
        x,y,z = q.popleft()
        if (x,y,z) in visited:
            continue
        visited.add((x,y,z))
        for dx,dy,dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            node = (x + dx, y + dy, z + dz)
            if (x + dx < min_x or x + dx > max_x or y + dy < min_y or y + dy > max_y or z + dz < min_z or z + dz > max_z):
                continue
            if node in cubes:
                print((x,y,z), (node))
                c += 1
                continue
            q.append(node)
    return c


# 1988 - Too low
# 1994 - Too low
# 1995 - too low
# 2888 - no

INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 58


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
