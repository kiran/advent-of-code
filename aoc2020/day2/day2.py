# import attr
from __future__ import annotations
import re
from typing import Optional, List

LINE_REGEX = re.compile("(\d+)-(\d+) ([a-z]): ([a-z]+)")

# @attr.s(auto_attribs=True)
class PasswordRule:
    # min_repeat: int
    # max_repeat: int
    # letter: str

    # password: str

    def __init__(self, min_repeat, max_repeat, letter, password):
        self.min_repeat = min_repeat
        self.max_repeat = max_repeat
        self.letter = letter

        self.password = password

    def check_validity(self, password: Optional[str] = None) -> bool:
        if password is None:
            password = self.password

        # char_count = password.count(self.letter)
        # if self.min_repeat <= char_count <= self.max_repeat:
        # 	return True

        if bool(password[self.min_repeat - 1] == self.letter) ^ bool(
            password[self.max_repeat - 1] == self.letter
        ):
            return True

        return False

    @classmethod
    def parse_from_line(cls, line: str) -> PasswordRule:
        m = re.match(LINE_REGEX, line)

        if m is None:
            raise ValueError(f"Could not parse line {line}")

        min_repeat, max_repeat, letter, password = m.group(1, 2, 3, 4)
        return PasswordRule(int(min_repeat), int(max_repeat), letter, password)


# rule = PasswordRule(1, 3, 'a', 'abcde')
# print(rule.check_validity())

# line = PasswordRule.parse_from_line('1-3 b: bcdefg')
# print(line.check_validity())

with open("./input.txt") as f:
    lines = f.read().splitlines()

password_formats: List[PasswordRule] = [
    PasswordRule.parse_from_line(line.strip()) for line in lines
]

valid_passwords: List[PasswordRule] = [
    x.password for x in password_formats if x.check_validity()
]
# print(valid_passwords)

print(len(valid_passwords))
