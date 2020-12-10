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


def count_ways(
    adapters: Set[int], current_value: int, cached_calculation: Dict[int, int]
):
    if current_value in cached_calculation:
        return cached_calculation[current_value]
    cached_calculation[current_value] = sum(
        [
            count_ways(adapters, i, cached_calculation)
            for i in range(current_value + 1, current_value + 4)
            if i in adapters
        ]
    )
    return cached_calculation[current_value]


def valid_combinations(adapters: List[int]) -> int:
    cached_calculation = {sorted(adapters)[-1]: 1}
    count_ways(set(adapters), 0, cached_calculation)
    return cached_calculation[0]


assert valid_combinations(adapters_for_input_file("minimal_input.txt")) == 8
assert valid_combinations(adapters_for_input_file("medium_input.txt")) == 19208

print(valid_combinations(adapters_for_input_file("input.txt")))
