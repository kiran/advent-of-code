from __future__ import annotations
import attr
from typing import Sequence
import math

MAX_ROWS = 127
MAX_COLS = 7


@attr.s(auto_attribs=True)
class Seat:
    row: int
    col: int

    @classmethod
    def from_seat_sequence(cls, seat_seq: str) -> Seat:
        spec = SeatSpecifier.from_seat_sequence(seat_seq)

        row = binary_space_partition(spec.row_spec, 0, MAX_ROWS)
        col = binary_space_partition(spec.col_spec, 0, MAX_COLS)

        return cls(row, col)

    @property
    def seat_id(self):
        return (8 * self.row) + self.col


@attr.s(auto_attribs=True)
class SeatSpecifier:
    row_spec: str
    col_spec: str

    @classmethod
    def from_seat_sequence(cls, seat_seq: str) -> SeatSpecifier:
        # replace F/B/L/R with up/down instead
        row_spec = seat_seq[:7].replace("F", "D").replace("B", "U")
        col_spec = seat_seq[7:].replace("L", "D").replace("R", "U")
        return cls(row_spec, col_spec)


def binary_space_partition(sequence: str, lo: int, hi: int) -> int:
    if lo == hi:
        return lo

    return binary_space_partition(sequence[1:], *new_range(sequence[0], lo, hi))


def new_range(char: str, lo: int, hi: int) -> Tuple[int, int]:
    midpoint = lo + math.ceil((hi - lo) / 2)
    if char == "D":
        return (lo, midpoint - 1)
    elif char == "U":
        return (midpoint, hi)
    else:
        raise ValueError(f"could not understand char {char}")


with open("./input.txt") as f:
    input_lines = f.read().splitlines()

max_seat_id = max(Seat.from_seat_sequence(line).seat_id for line in input_lines)
print(max_seat_id)

# assert Seat(70, 7).seat_id == 567
# assert Seat(14, 7).seat_id == 119
# assert Seat(102, 4).seat_id == 820

# assert SeatSpecifier.from_seat_sequence("BFFFBBFRRR") == SeatSpecifier(
#     row_spec="UDDDUUD", col_spec="UUU"
# ), SeatSpecifier.from_seat_sequence("BFFFBBFRRR")
# assert new_range("D", 0, 127) == (0, 63), new_range("D", 0, 127)
# assert new_range("U", 0, 63) == (32, 63), new_range("U", 0, 63)
# assert new_range("U", 32, 47) == (40, 47), new_range("U", 32, 47)
# assert binary_space_partition("UDU", 0, MAX_COLS) == 5

# assert Seat.from_seat_sequence("BFFFBBFRRR") == Seat(70, 7)
# assert Seat.from_seat_sequence("FFFBBBFRRR") == Seat(14, 7)
# assert Seat.from_seat_sequence("BBFFBBFRLL") == Seat(102, 4)
