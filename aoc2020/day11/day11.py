from __future__ import annotations
import attr
from enum import Enum

from typing import List


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
    def from_input_lines(cls, lines):
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

        adjacent_occupied = self.count_adjacenct_occupied(row, col, SeatState.occupied)

        if current_state == SeatState.empty:
            if adjacent_occupied == 0:
                return SeatState.occupied
            return SeatState.empty
        elif current_state == SeatState.occupied:
            if adjacent_occupied >= 4:
                return SeatState.empty
            return SeatState.occupied
        else:
            raise NotImplementedError(f"Unclear seat state: {current_state}")

    def count_adjacenct_occupied(
        self, row: int, col: int, state: SeatState = SeatState.occupied
    ) -> int:
        """
        Count how many adjacent seats are in the state.
        """
        num_rows = len(self.seats)
        num_cols = len(self.seats[0])

        adjacent_coords = filter(
            lambda coord: (0 <= coord[0] < num_rows) and (0 <= coord[1] < num_cols),
            [
                (row + 1, col),
                (row + 1, col + 1),
                (row + 1, col - 1),
                (row, col + 1),
                (row, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row - 1, col - 1),
            ],
        )

        occupied = 0
        for row, col in adjacent_coords:
            if self.seats[row][col] == state:
                occupied += 1
        return occupied


def find_stable_ferry(ferry: Ferry) -> Ferry:
    next_round = ferry.next_round()
    while ferry != next_round:
        ferry = next_round
        next_round = ferry.next_round()

    return ferry


# ------------------------------------------------

with open("./minimal_input.txt") as f:
    input_lines = f.read().splitlines()

test_ferry = Ferry.from_input_lines(input_lines)
assert test_ferry.to_str() == "\n".join(input_lines)
assert test_ferry.num_occupied == 0
stable_ferry = find_stable_ferry(test_ferry)
assert stable_ferry.num_occupied == 37

# ------------------------------------------------

with open("./input.txt") as f:
    input_lines = f.read().splitlines()

ferry = Ferry.from_input_lines(input_lines)
stable_ferry = find_stable_ferry(ferry)

print(stable_ferry.num_occupied)
