from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Shape:
    def __init__(self, shape):
        self.shape = []
        if shape == "####":
            self.shape.extend([(x, 0) for x in range(4)])
        elif shape == ".#.\n###\n.#.":
            self.shape = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
        elif shape == "..#\n..#\n###":
            self.shape.append((0, 0))
            self.shape.append((1, 0))
            self.shape.append((2, 0))
            self.shape.append((2, 1))
            self.shape.append((2, 2))
        elif shape == "#\n#\n#\n#":
            self.shape.append((0, 0))
            self.shape.append((0, 1))
            self.shape.append((0, 2))
            self.shape.append((0, 3))
        elif shape == "##\n##":
            self.shape.append((0, 0))
            self.shape.append((1, 0))
            self.shape.append((0, 1))
            self.shape.append((1, 1))
        self.shape_raw = shape

    def move_wind(self, wind_dir, shape_pos, board):
        x, y = shape_pos
        if wind_dir == ">":
            d = 1
        else:
            d = -1
        for sx, sy in self.shape:
            new_x = x + sx + d
            if new_x < 0 or new_x > 6:
                return False
            if board[new_x, y + sy] == "#":
                return False
        return True

    def move_down(self, shape_pos, board):
        x, y = shape_pos
        for sx, sy in self.shape:
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


def create_board_sig(line_count, max_y, board):
    res = ""
    for y in range(line_count):
        for x in range(7):
            res += board[x,y + max_y]
    return res


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
    cache = {}
    i = 0
    add = 0
    n = 1000000000000
    while i < n:
        max_y = max([y for (x, y), val in board.items() if val == "#"])
        rock_id = i % 5
        shape = shapes[rock_id]
        board_sig = create_board_sig(30, max_y, board)
        sig = (rock_id, wind_i, board_sig)
        if sig in cache:
            old_i, old_max_y = cache[sig]
            diff_i = i - old_i
            diff_h = max_y - old_max_y
            reps = (n - i) // diff_i
            add += diff_h * reps
            i += reps * diff_i
            print(diff_i, n-i, add)
            cache = {}
        cache[rock_id, wind_i, board_sig] = i, max_y
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
    return max_y + add

INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 1514285714288


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
