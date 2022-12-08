from __future__ import annotations

from collections import deque, Counter
import argparse
import os.path
from dataclasses import dataclass
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Directory:
    def __init__(self, name):
        self.name = name
        self.dirs = {}
        self.size = 0
        self.files = []
        self.parent = None

    def add_file(self, size):
        self.size += size
        if self.parent:
            self.parent.add_file(size)

    def add_dir(self, name):
        d = Directory(name)
        d.parent = self
        self.dirs[name] = d





def compute(s: str) -> int:
    root = Directory("/")
    i = 1
    lines = s.splitlines()
    cur = root
    while i < len(lines):
        line = lines[i]
        print(lines[i])
        if line == "$ ls":
            i += 1
            while i < len(lines) and lines[i] and not lines[i].startswith("$"):
                line = lines[i]
                if line.startswith("dir"):
                    name = line.split()[1]
                    cur.add_dir(name)
                else:
                    assert line[0].isdigit()
                    size, name = line.split()
                    cur.add_file(int(size))
                i += 1
        elif line.startswith("$ cd"):
            name = line.split()[2]
            if name == "..":
                cur = cur.parent
            else:
                cur = cur.dirs[name]
            i+=1
        else:
            assert False, line
    res = bfs(root, 100000)

    return res


def bfs(root, size):
    res = 0
    if root is None:
        return 0
    if root.size < size:
        res+=root.size
    for dir in root.dirs.values():
        res += bfs(dir, size)
    return res

INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
