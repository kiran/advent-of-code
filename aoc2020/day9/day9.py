from typing import List, Set


def has_valid_sum(number: int, preamble: Set[int]) -> bool:
    found_valid_sum = False
    for candidate in preamble:
        if (number - candidate) in preamble:
            found_valid_sum = True
            break
    return found_valid_sum


preamble = {1, 20, 25}
assert has_valid_sum(26, preamble)
assert has_valid_sum(21, preamble)
assert has_valid_sum(25, preamble) == False


def find_first_invalid_msg(numbers: List[int], window: int) -> int:
    for i in range(window, len(numbers)):
        preamble = set(numbers[i - window : i])
        if not has_valid_sum(numbers[i], preamble):
            return numbers[i]

    raise ValueError("found no invalid msg")


def find_contiguous_range_that_sums_to(target: int, numbers: List[int]) -> List[int]:
    for i in range(len(numbers)):
        sum_so_far = numbers[i]
        for j in range(i + 1, len(numbers)):
            sum_so_far += numbers[j]

            if sum_so_far == target:
                return numbers[i : j + 1]
            elif sum_so_far > target:
                break

    raise ValueError(f"No contiguous range sums to {target}")


def find_encryption_weakness(numbers: List[int], window: int) -> int:
    invalid_msg = find_first_invalid_msg(numbers, window)
    contiguous_range = find_contiguous_range_that_sums_to(invalid_msg, numbers)
    weakness = min(contiguous_range) + max(contiguous_range)

    return weakness


with open("./minimal_input.txt") as f:
    input_lines = f.read().splitlines()

messages = [int(line) for line in input_lines]

assert find_first_invalid_msg(messages, 5) == 127

assert find_contiguous_range_that_sums_to(127, messages) == [15, 25, 47, 40]
assert find_contiguous_range_that_sums_to(215, messages) == [55, 65, 95]
assert find_contiguous_range_that_sums_to(449, messages) == [117, 150, 182]

assert find_encryption_weakness(messages, 5) == 62

with open("./input.txt") as f:
    input_lines = f.read().splitlines()

messages = [int(line) for line in input_lines]

print(f"Weakness: {find_encryption_weakness(messages, 25)}")
