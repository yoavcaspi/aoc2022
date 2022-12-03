from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    m = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    res = {}

    res[("A", "Z")] = 2 + 6
    res[("B", "Z")] = 3 + 6
    res[("C", "Z")] = 1 + 6
    res[("A", "Y")] = 1 + 3
    res[("B", "Y")] = 2 + 3
    res[("C", "Y")] = 3 + 3
    res[("A", "X")] = 3
    res[("B", "X")] = 1
    res[("C", "X")] = 2
    tot = 0
    for line in s.strip().split("\n"):
        a,b = line.split()
        tot += res[(a,b)]
    return tot


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
