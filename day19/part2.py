from __future__ import annotations

import argparse
import functools
import os.path
import re
from collections import defaultdict, deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # Blueprint 1: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 2 ore and 15 obsidian.
    blueprints = []
    print()
    pattern = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
    res = 1
    for line in s.strip().splitlines()[:3]:
        groups=pattern.match(line).groups()
        i = int(groups[0])
        ore_robot_ore = int(groups[1])
        clay_robot_ore = int(groups[2])
        obsidian_robot_ore = int(groups[3])
        obsidian_robot_clay = int(groups[4])
        geode_robot_ore = int(groups[5])
        geode_robot_obs = int(groups[6])

        def can_create_r_ore(o):
            return o >= ore_robot_ore

        def can_create_r_clay(o):
            return o >= clay_robot_ore

        def can_create_r_obs(o, c):
            return o >= obsidian_robot_ore and c >= obsidian_robot_clay

        def can_create_r_geode(o, obs):
            return o >= geode_robot_ore and obs >= geode_robot_obs


        @functools.cache
        def find_max(m, ore, clay, obsidian, geode, r_ore, r_clay, r_obsidian, r_geode):
            if m == 0:
                return geode

            max_val = geode

            if can_create_r_geode(ore, obsidian):
                return find_max(m - 1, ore + r_ore - geode_robot_ore, clay + r_clay, obsidian + r_obsidian - geode_robot_obs,
                          geode + r_geode, r_ore, r_clay, r_obsidian, r_geode + 1)

            if can_create_r_ore(ore):
                if (ore + r_ore) < max(obsidian_robot_ore, clay_robot_ore, geode_robot_ore) * m:
                    max_val = max(max_val, find_max(m - 1, ore + r_ore - ore_robot_ore, clay + r_clay, obsidian + r_obsidian, geode + r_geode, r_ore + 1, r_clay, r_obsidian, r_geode))
            if can_create_r_clay(ore):
                if (clay + r_clay) < (obsidian_robot_clay * m):
                    max_val = max(max_val, find_max(m - 1, ore + r_ore - clay_robot_ore, clay + r_clay, obsidian + r_obsidian, geode + r_geode,
                              r_ore, r_clay + 1, r_obsidian, r_geode))
            if can_create_r_obs(ore, clay):
                if (obsidian + r_obsidian) < (geode_robot_obs * m):
                    max_val = max(max_val, find_max(
                             m - 1, ore + r_ore - obsidian_robot_ore, clay + r_clay - obsidian_robot_clay, obsidian + r_obsidian,
                             geode + r_geode, r_ore, r_clay, r_obsidian + 1, r_geode))
            if ore + r_ore - ore_robot_ore < max(clay_robot_ore, obsidian_robot_ore, geode_robot_ore) and ore < ore_robot_ore:
                max_val = max(max_val, find_max(m - 1, ore + r_ore, clay + r_clay, obsidian + r_obsidian, geode + r_geode, r_ore, r_clay, r_obsidian, r_geode))
            return max_val
        # m, ore, clay, obsidian, geode, r_ore, r_clay, r_obsidian, r_geode
        val = find_max(32, 0, 0, 0, 0, 1, 0, 0, 0)
        print(val)
        res *= val
    return res


# 1988 - Too low
# 1994 - Too low
# 1995 - too low
# 2888 - no

INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''
EXPECTED = 3472


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
