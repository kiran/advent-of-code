from typing import Set, Tuple, cast
import itertools

with open("./input.txt") as f:
    lines = f.read().splitlines()

expenses = [int(line.strip()) for line in lines]


options: Set[Tuple[int, int, int]] = set()

for a, b, c in itertools.permutations(expenses, 3):
    if a + b + c == 2020:
        sorted_tuple = cast(Tuple[int, int, int], tuple(sorted([a, b, c])))
        options.add(sorted_tuple)

print(options)

assert len(options) == 1

a, b, c = options.pop()

print(a * b * c)
