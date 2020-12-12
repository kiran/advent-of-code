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

    # the waypoint's position is defined relative to the ship
    waypoint_horiz: int
    waypoint_vert: int

    @property
    def manhattan_distance(self) -> int:
        return abs(self.horiz) + abs(self.vert)

    def move(self, command: Command) -> Position:
        """
        Action N means to move the waypoint north by the given value.
        Action S means to move the waypoint south by the given value.
        Action E means to move the waypoint east by the given value.
        Action W means to move the waypoint west by the given value.
        Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
        Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
        Action F means to move forward to the waypoint a number of times equal to the given value.
        """
        if command.action == "N":
            return attr.evolve(self, waypoint_vert=self.waypoint_vert + command.value)
        elif command.action == "S":
            return attr.evolve(self, waypoint_vert=self.waypoint_vert - command.value)
        elif command.action == "E":
            return attr.evolve(self, waypoint_horiz=self.waypoint_horiz + command.value)
        elif command.action == "W":
            return attr.evolve(self, waypoint_horiz=self.waypoint_horiz - command.value)
        elif command.action == "R":
            return self.move_waypoint_around_ship(-command.value)
        elif command.action == "L":
            return self.move_waypoint_around_ship(command.value)
        elif command.action == "F":
            horiz = self.horiz + (command.value * self.waypoint_horiz)
            vert = self.vert + (command.value * self.waypoint_vert)
            return attr.evolve(self, horiz=horiz, vert=vert)
        else:
            raise NotImplementedError(f"todo: {command}")

    def move_waypoint_around_ship(self, degrees: int) -> Position:
        """
        TIME FOR SOME TRIG

        note: this rotates counter-clockwise
        """
        radians = math.radians(degrees)
        x = self.waypoint_horiz
        y = self.waypoint_vert

        xx = int(x * math.cos(radians)) - int(y * math.sin(radians))
        yy = int(x * math.sin(radians)) + int(y * math.cos(radians))

        return attr.evolve(self, waypoint_horiz=xx, waypoint_vert=yy)


def positions_from_file(filename: str, debug: bool = False) -> List[Position]:
    commands = commands_from_file(filename)
    positions = [Position(0, 0, 10, 1)]

    for command in commands:
        new_pos = positions[-1].move(command)
        positions.append(new_pos)
        if debug:
            print(command, new_pos)

    return positions


if __name__ == "__main__":

    assert Position(17, 8, 0, 0).manhattan_distance == 25

    positions = positions_from_file("minimal_input.txt")
    assert positions[-1].manhattan_distance == 286

    positions = positions_from_file("input.txt", debug=False)
    print(positions[-1].manhattan_distance)
