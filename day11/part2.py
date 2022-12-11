from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def func(val1, o, b):
    if b.isnumeric():
        val2 = int(b)
    else:
        assert b == "old"
        val2 = val1
    if o == "+":
        return val1 + val2
    elif o == "*":
        return val1 * val2
    else:
        assert False

class Monkey:
    def __init__(self):
        self.inspections = 0
        self.vals = []
        self.op = None
        self.test_num = None
        self.throw_to_true = None
        self.throw_to_false = None


def compute(s: str) -> int:
    monkeys = []
    print()
    for m in s.strip().split("\n\n"):
        monkey = Monkey()

        for line in m.split("\n")[1:]:
            if line.lstrip().startswith("Starting items:"):
                _, items = line.split(":")
                monkey.vals = [int(val) for val in items.split(",")]
            elif line.lstrip().startswith("Operation:"):
                _, items = line.split("=")
                a,o,b = items.split()
                assert a == "old"
                monkey.op = o
                monkey.val2 = b
            elif line.lstrip().startswith("Test:"):
                _, val = line.split("by ")
                monkey.test_num = int(val)
            elif line.lstrip().startswith("If true:"):
                _, val = line.split("monkey ")
                monkey.throw_to_true = int(val)
            elif line.lstrip().startswith("If false:"):
                _, val = line.split("monkey ")
                monkey.throw_to_false = int(val)
        monkeys.append(monkey)
    max_val = 1
    for m in monkeys:
        max_val*=m.test_num
    print()
    for i in range(1,10_001):
        for monkey in monkeys:
            while monkey.vals:
                monkey.inspections += 1
                item = monkey.vals.pop(0)
                item = func(item, monkey.op, monkey.val2)
                item = item % max_val
                if item % monkey.test_num == 0:
                    monkeys[monkey.throw_to_true].vals.append(item)
                else:
                    monkeys[monkey.throw_to_false].vals.append(item)
        if i in (1,20,1000,2000):
            print([m.inspections for m in monkeys])
    vals = sorted([m.inspections for m in monkeys])[-2:]
    return vals[0] * vals[1]



INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
