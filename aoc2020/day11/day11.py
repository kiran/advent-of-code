from __future__ import annotations
import attr
from enum import Enum

from typing import List, Tuple, Callable


class SeatState(Enum):
    empty = "L"
    occupied = "#"
    floor = "."

    @staticmethod
    def from_str(label):
        if label == "L":
            return SeatState.empty
        elif label == "#":
            return SeatState.occupied
        elif label == ".":
            return SeatState.floor
        else:
            raise NotImplementedError(f"No seat state for {label}")


@attr.s(auto_attribs=True, frozen=True)
class Ferry:
    seats: List[List[SeatState]]

    @classmethod
    def from_input_file(cls, filename: str):
        with open(filename) as f:
            input_lines = f.read().splitlines()

        seats: List[List[SeatState]] = []
        for line in input_lines:
            row = [SeatState.from_str(char) for char in line.strip()]
            seats.append(row)

        return Ferry(seats)

    def to_str(self) -> str:
        return "\n".join("".join(seat.value for seat in row) for row in self.seats)

    @property
    def num_occupied(self) -> int:
        return sum(
            sum(seat == SeatState.occupied for seat in row) for row in self.seats
        )

    def next_round(self) -> Ferry:
        new_seats: List[List[SeatState]] = []

        num_rows = len(self.seats)
        num_cols = len(self.seats[0])

        for row in range(num_rows):
            new_seats.append([self.next_value(row, col) for col in range(num_cols)])
        return Ferry(new_seats)

    def next_value(self, row: int, col: int) -> SeatState:
        """
        Calculate the seat state at [row, col] in the next round:

        If a seat is empty (L) and there are no occupied seats adjacent to it,
        the seat becomes occupied.

        If a seat is occupied (#) and four or more seats adjacent to it are
        also occupied, the seat becomes empty.

        Otherwise, the seat's state does not change.
        """
        current_state = self.seats[row][col]

        if current_state == SeatState.floor:
            return current_state

        adjacent_occupied = self.count_occupied_in_directions(row, col)

        if current_state == SeatState.empty:
            if adjacent_occupied == 0:
                return SeatState.occupied
            return SeatState.empty
        elif current_state == SeatState.occupied:
            if adjacent_occupied >= 5:
                return SeatState.empty
            return SeatState.occupied
        else:
            raise NotImplementedError(f"Unclear seat state: {current_state}")

    def count_occupied_in_directions(self, row: int, col: int) -> int:
        """
        Count how many adjacent seats are in the state.
        """
        coord = (row, col)

        transforms = [
            lambda coord: (coord[0] + 1, coord[1]),
            lambda coord: (coord[0] + 1, coord[1] + 1),
            lambda coord: (coord[0] + 1, coord[1] - 1),
            lambda coord: (coord[0], coord[1] + 1),
            lambda coord: (coord[0], coord[1] - 1),
            lambda coord: (coord[0] - 1, coord[1]),
            lambda coord: (coord[0] - 1, coord[1] + 1),
            lambda coord: (coord[0] - 1, coord[1] - 1),
        ]

        occupied = 0
        for transform in transforms:
            if self.state_of_first_chair(coord, transform) == SeatState.occupied:
                occupied += 1

        return occupied

    def state_of_first_chair(
        self,
        coord: Tuple[int, int],
        transform: Callable[[Tuple[int, int]], Tuple[int, int]],
    ) -> SeatState:
        """
        Return the seat state of the first non-floor seat we see,
        or return floor if there are no seats in that direction.

        TODO: cache the location of the first chair for a given coord
        """
        num_rows = len(self.seats)
        num_cols = len(self.seats[0])
        coord_valid = lambda coord: (0 <= coord[0] < num_rows) and (
            0 <= coord[1] < num_cols
        )

        new_coord = transform(coord)
        while coord_valid(new_coord):
            chair_val = self.seats[new_coord[0]][new_coord[1]]

            if chair_val != SeatState.floor:
                return chair_val

            coord = new_coord
            new_coord = transform(coord)

        return SeatState.floor


def find_stable_ferry(ferry: Ferry) -> Ferry:
    next_round = ferry.next_round()
    while ferry != next_round:
        ferry = next_round
        next_round = ferry.next_round()

    return ferry


# ------------------------------------------------

test_ferry = Ferry.from_input_file("minimal_input.txt")
stable_ferry = find_stable_ferry(test_ferry)
assert stable_ferry.num_occupied == 26
assert stable_ferry == Ferry.from_input_file("minimal_input_stabilized.txt")

# ------------------------------------------------


test_ferry = Ferry.from_input_file("input.txt")
stable_ferry = find_stable_ferry(test_ferry)

print(stable_ferry.num_occupied)
