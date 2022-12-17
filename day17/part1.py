from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Shape:
    def __init__(self, shape):
        self.left = []
        self.bottom = []
        self.right = []
        self.shape = []
        if shape == "####":
            self.left.append((0, 0))
            self.bottom.extend([(x, 0) for x in range(4)])
            self.shape.extend([(x, 0) for x in range(4)])
            self.right.append((3, 0))
        elif shape == ".#.\n###\n.#.":
            self.left.append((1, 0))
            self.left.append((0, 1))
            self.left.append((1, 2))

            self.bottom.append((0, 1))
            self.bottom.append((1, 0))
            self.bottom.append((2, 1))

            self.shape = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]

            self.right.append((1, 0))
            self.right.append((2, 1))
            self.right.append((1, 2))
        elif shape == "..#\n..#\n###":
            self.left.append((0, 0))
            self.left.append((2, 1))
            self.left.append((2, 2))

            self.bottom.append((0, 0))
            self.bottom.append((1, 0))
            self.bottom.append((2, 0))

            self.shape.append((0, 0))
            self.shape.append((1, 0))
            self.shape.append((2, 0))
            self.shape.append((2, 1))
            self.shape.append((2, 2))

            self.right.append((2, 0))
            self.right.append((2, 1))
            self.right.append((2, 2))
        elif shape == "#\n#\n#\n#":
            self.left.append((0, 0))
            self.left.append((0, 1))
            self.left.append((0, 2))
            self.left.append((0, 3))

            self.bottom.append((0, 0))

            self.shape.append((0, 0))
            self.shape.append((0, 1))
            self.shape.append((0, 2))
            self.shape.append((0, 3))

            self.right.append((0, 0))
            self.right.append((0, 1))
            self.right.append((0, 2))
            self.right.append((0, 3))
        elif shape == "##\n##":
            self.left.append((0, 0))
            self.left.append((0, 1))

            self.bottom.append((0, 0))
            self.bottom.append((1, 0))

            self.shape.append((0, 0))
            self.shape.append((1, 0))
            self.shape.append((0, 1))
            self.shape.append((1, 1))

            self.right.append((1, 0))
            self.right.append((1, 1))
        self.shape_raw = shape

    def move_wind(self, wind_dir, shape_pos, board):
        x, y = shape_pos
        if wind_dir == ">":
            d = 1
            d_list = self.right
        else:
            d = -1
            d_list = self.left
        for sx, sy in d_list:
            new_x = x + sx + d
            if new_x < 0 or new_x > 6:
                return False
            if board[new_x, y + sy] == "#":
                return False
        return True

    def move_down(self, shape_pos, board):
        x, y = shape_pos
        for sx, sy in self.bottom:
            if board[x + sx, y + sy - 1] == "#":
                return False
        return True


def place_shape(board, shape_pos, shape):
    for x, y in shape.shape:
        sx, sy = shape_pos
        new_x = sx + x
        new_y = sy + y
        assert board[new_x,new_y] == "."
        board[new_x, new_y] = "#"


def compute(s: str) -> int:
    shapes_raw = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
    """
    shapes = []
    for shape in shapes_raw.split("\n\n"):
        shapes.append(Shape(shape.strip()))

    board = defaultdict(lambda: ".")
    for x in range(7):
        board[x, 0] = "#"
    wind = s.strip()
    wind_i = 0
    i = 0
    n = 2022
    while i < n:
        max_y = max([y for (x, y), val in board.items() if val == "#"])
        shape = shapes[i % 5]
        shape_pos = (2, max_y + 4)
        while True:
            wind_dir = wind[wind_i]
            wind_i = (wind_i + 1) % len(wind)
            if shape.move_wind(wind_dir, shape_pos, board):
                if wind_dir == ">":
                    new_x = shape_pos[0] + 1
                else:
                    new_x = shape_pos[0] - 1
                shape_pos = (new_x, shape_pos[1])
            if shape.move_down(shape_pos, board):
                shape_pos = (shape_pos[0], shape_pos[1] - 1)
            else:
                place_shape(board, shape_pos, shape)
                break
        i += 1
    max_y = max([y for (x, y), val in board.items() if val == "#"])
    return max_y


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 3068


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
