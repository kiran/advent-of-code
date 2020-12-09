from __future__ import annotations
import attr
from typing import Sequence
import math

# is this a fancy bit manipulation algorithm?

MAX_ROWS = 127
MAX_COLS = 7


@attr.s(auto_attribs=True)
class Seat:
    row: int
    col: int

    @classmethod
    def from_seat_sequence(cls, seat_seq: str) -> Seat:
        row_spec = seat_seq[:7].replace("F", "0").replace("B", "1")
        col_spec = seat_seq[7:].replace("L", "0").replace("R", "1")

        row = int(row_spec, 2)
        col = int(col_spec, 2)

        return cls(row, col)

    @classmethod
    def from_seat_id(cls, seat_id: int) -> Seat:
        seq = f"{seat_id:010b}"
        row = int(seq[:7], 2)
        col = int(seq[7:], 2)

        return cls(row, col)

    @property
    def seat_id(self):
        return (8 * self.row) + self.col


assert Seat(70, 7).seat_id == 567
assert Seat.from_seat_id(567) == Seat(70, 7)
assert Seat(14, 7).seat_id == 119
assert Seat(102, 4).seat_id == 820

assert Seat.from_seat_sequence("BFFFBBFRRR") == Seat(70, 7)
assert Seat.from_seat_sequence("FFFBBBFRRR") == Seat(14, 7)
assert Seat.from_seat_sequence("BBFFBBFRLL") == Seat(102, 4)


with open("./input.txt") as f:
    input_lines = f.read().splitlines()

avail_seats = set(range(0, Seat(MAX_ROWS, MAX_COLS).seat_id + 1))
taken_seats = {Seat.from_seat_sequence(line).seat_id for line in input_lines}
potential_seat_ids = avail_seats - taken_seats

seats_with_occupied_neighbors = set()
for seat in potential_seat_ids:
    if not (seat + 1 in potential_seat_ids or seat - 1 in potential_seat_ids):
        seats_with_occupied_neighbors.add(seat)

print(seats_with_occupied_neighbors)
