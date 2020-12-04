from typing import Set, Tuple
import itertools

with open("./input.txt") as f:
    lines = f.read().splitlines()

expenses = [int(line.strip()) for line in lines]


options: Set[Tuple[int, int]] = set()

for a, b, c in itertools.permutations(expenses, 3):
    if a + b + c == 2020:
        options.add(tuple(sorted([a, b, c])))

print(options)

assert len(options) == 1

a, b, c = options.pop()

print(a * b * c)
