from __future__ import annotations

import argparse
import ast
import os.path
from collections import defaultdict
from itertools import zip_longest

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_next_val(packet):
    vals = ast.literal_eval(packet)
    for val in vals:
        yield val


def compare(left_it, right_it):
    for left, right in zip_longest(left_it, right_it, fillvalue=""):
        if left == "":
            return 1
        if right == "":
            return -1
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return -1
        elif isinstance(left, list) and isinstance(right, list):
            res = compare(left, right)
            if res != 0:
                return res
        elif isinstance(left, list) and isinstance(right, int):
            res = compare(left, [right])
            if res != 0:
                return res
        elif isinstance(left, int) and isinstance(right, list):
            res = compare([left], right)
            if res != 0:
                return res
        else:
            assert False, f"{left=} {right=}"

    return 0


def compute(s: str) -> int:
    res = 0
    for i, pair in enumerate(s.strip().split("\n\n"), start=1):
        left, right = pair.splitlines()
        left_it = get_next_val(left)
        right_it = get_next_val(right)
        c = compare(left_it, right_it)
        if c == 1:
            res += i

    return res


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 13


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
