from __future__ import annotations

import attr
from decimal import Decimal
import math
import re
from typing import List, Sequence

ACTION_REGEX = re.compile("([NSEWLRF])(\d+)")


@attr.s(auto_attribs=True)
class Command:
    action: str
    value: int

    @classmethod
    def from_line(cls, line: str) -> Command:
        m = re.match(ACTION_REGEX, line)

        if m is None:
            raise ValueError(f"Could not parse line {line}")

        action = m.group(1)
        value = int(m.group(2))

        return Command(action, value)


def commands_from_file(filename: str) -> Sequence[Command]:
    with open(filename) as f:
        input_lines = f.read().splitlines()

    return [Command.from_line(line) for line in input_lines]


@attr.s(auto_attribs=True, frozen=True)
class Position:
    horiz: int
    vert: int

    # heading in degrees
    # todo: validator?
    heading: int

    @property
    def manhattan_distance(self) -> int:
        return abs(self.horiz) + abs(self.vert)

    def move(self, command: Command) -> Position:
        """
        N means to move north by the given value.
        S means to move south by the given value.
        E means to move east by the given value.
        W means to move west by the given value.
        L means to turn left the given number of degrees.
        R means to turn right the given number of degrees.
        F means to move forward by the given value in the direction the ship is currently facing.
        """
        if command.action == "N":
            return attr.evolve(self, vert=self.vert + command.value)
        elif command.action == "S":
            return attr.evolve(self, vert=self.vert - command.value)
        elif command.action == "E":
            return attr.evolve(self, horiz=self.horiz + command.value)
        elif command.action == "W":
            return attr.evolve(self, horiz=self.horiz - command.value)
        elif command.action == "R":
            new_heading = (self.heading - command.value) % 360
            return attr.evolve(self, heading=new_heading)
        elif command.action == "L":
            new_heading = (self.heading + command.value) % 360
            return attr.evolve(self, heading=new_heading)
        elif command.action == "F":
            rads = math.radians(self.heading)
            horiz = self.horiz + int(math.cos(rads) * command.value)
            vert = self.vert + int(math.sin(rads) * command.value)
            return attr.evolve(self, horiz=horiz, vert=vert)
        else:
            raise NotImplementedError(f"todo: {command}")


def positions_from_file(filename: str, debug: bool = False) -> List[Position]:
    commands = commands_from_file(filename)
    positions = [Position(0, 0, 0)]

    for command in commands:
        new_pos = positions[-1].move(command)
        positions.append(new_pos)
        if debug:
            print(new_pos)

    return positions


if __name__ == "__main__":

    assert Position(17, 8, 0).manhattan_distance == 25

    positions = positions_from_file("minimal_input.txt")
    assert positions[-1].manhattan_distance == 25

    positions = positions_from_file("input.txt", debug=False)
    print(positions[-1].manhattan_distance)
