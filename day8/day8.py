import attr
from typing import List


@attr.s(auto_attribs=True, frozen=True)
class Instruction:
    line_no: int
    operation: str
    value: int


class InfiniteLoopException(Exception):
    pass


def execute_instructions(instructions: List[Instruction], debug: bool = False) -> int:
    visited_instructions = set()
    accumulator = 0

    pc = 0
    step = 0

    while pc < len(instructions):
        step += 1
        inst = instructions[pc]
        if debug:
            print(f"instruction: {inst} pc: {pc} step: {step} acc: {accumulator}")

        if inst in visited_instructions:
            raise InfiniteLoopException(f"Visited instruction a second time! Breaking.")

        visited_instructions.add(inst)

        if inst.operation == "nop":
            pc += 1
        elif inst.operation == "acc":
            accumulator += inst.value
            pc += 1
        elif inst.operation == "jmp":
            pc += inst.value
        else:
            raise ValueError(f"Invalid instruction: {inst.operation}")

    return accumulator


def parse_instruction(line: str, line_no: int) -> Instruction:
    operation, val = line.split(" ")
    return Instruction(line_no, operation, int(val))


def brute_force_fix_corruption(instructions: List[Instruction]) -> None:
    for i, inst in enumerate(instructions):
        if inst.operation == "nop":
            continue

        trial = instructions.copy()
        new_op = "nop"
        if inst.operation == "nop":
            new_op = "jmp"
        trial[i] = Instruction(i, new_op, inst.value)

        try:
            acc_value = execute_instructions(trial)
        except InfiniteLoopException:
            continue
        else:
            print(f"We're done! changed_inst: {i} acc: {acc_value}")
            break


with open("./input.txt") as f:
    input_lines = f.read().splitlines()

instructions = [parse_instruction(line, i) for i, line in enumerate(input_lines)]
# execute_instructions(instructions, debug=True)
brute_force_fix_corruption(instructions)
