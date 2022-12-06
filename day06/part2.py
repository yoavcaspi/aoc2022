from __future__ import annotations

from collections import deque, Counter
import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    count = 14
    val = deque()
    res = 0
    for c in s:
        res += 1
        if len(val) < count:
            val.append(c)
        else:
            val.popleft()
            val.append(c)
            if len(Counter(val)) == count:
                return res
    return res


INPUT_S = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED = 19


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26)
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
