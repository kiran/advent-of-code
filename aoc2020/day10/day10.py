from typing import Dict, List, Set, Tuple
from collections import defaultdict
import itertools
import math

TOLERANCE = 3


def chain_adapters(adapters: List[int]) -> List[int]:
    built_in_adapter = max(adapters) + 3
    adapters.append(0)
    adapters.append(built_in_adapter)
    return sorted(adapters)


def count_differences(sorted_adapters: List[int]) -> Dict[int, int]:
    differences: Dict[int, int] = defaultdict(lambda: 0)

    for i in range(1, len(sorted_adapters)):
        diff = sorted_adapters[i] - sorted_adapters[i - 1]
        differences[diff] += 1

    return differences


def validate_differences(sorted_adapters: List[int]) -> bool:
    for i in range(1, len(sorted_adapters)):
        if sorted_adapters[i] - sorted_adapters[i - 1] > TOLERANCE:
            return False
    return True


def adapters_for_input_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        input_lines = f.read().splitlines()

    return [int(line) for line in input_lines]


def diff_dist_for_input_file(file_name: str) -> Dict[int, int]:
    return count_differences(chain_adapters(adapters_for_input_file(file_name)))


# assert diff_dist_for_input_file("minimal_input.txt") == {1: 7, 3: 5}
# assert diff_dist_for_input_file("medium_input.txt") == {1: 22, 3: 10}

# diff_dist = diff_dist_for_input_file("input.txt")
# print(diff_dist[1] * diff_dist[3])


def combo2(lst: List[int], n: int, prev_el=0):
    if n == 0:
        return [[]]
    l = []
    for i in range(0, len(lst)):
        m = lst[i]
        if m - prev_el > TOLERANCE:
            break

        remLst = lst[i + 1 :]

        for p in combo2(remLst, n - 1, m):
            l.append([m] + p)
    return l


def valid_combinations(adapters: List[int]) -> int:
    valid_options = 0

    sorted_adapters = sorted(adapters)
    target = sorted_adapters[-1] + 3

    min_steps = math.ceil(target / 3)

    for r in range(min_steps, len(sorted_adapters) + 1):
        print(f"Trying candidates of len {r} / {len(sorted_adapters)}")
        for option in combo2(sorted_adapters, r):
            if target - option[-1] <= TOLERANCE:
                valid_options += 1

        print(f"Found {valid_options} candidates so far.")

    return valid_options


# valid_combinations([5, 8, 10])
assert valid_combinations(adapters_for_input_file("minimal_input.txt")) == 8
assert valid_combinations(adapters_for_input_file("medium_input.txt")) == 19208

# print(valid_combinations(adapters_for_input_file("input.txt")))
