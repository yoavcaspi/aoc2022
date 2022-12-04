from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    tot=0
    for line in s.splitlines():
        first_part, second_part = line.split(",")
        a,b = first_part.split("-")
        c,d = second_part.split("-")
        print(first_part, second_part)
        first_set = set(list(range(int(a),int(b) + 1)))
        second_set = set(list(range(int(c),int(d) + 1)))
        if first_set == second_set:
            print("^^^^")
        if first_set <= second_set:
            tot+=1
        elif second_set <= first_set:
            tot+=1
    return tot


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2


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
