from typing import Dict
import re

required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

with open("./input.txt") as f:
    passport_batch = f.read().split("\n\n")


def parse_record_from_line(batch_line: str) -> Dict[str, str]:
    key_pairs = batch_line.split()
    passport_record = {}
    for key_pair in key_pairs:
        key, value = key_pair.split(":")
        passport_record[key] = value
    return passport_record


def check_birth_year(passport_record) -> bool:
    byr = int(passport_record["byr"])
    if not (1920 <= byr <= 2002):
        print(f"byr invalid: {byr}")
        return False
    return True


def check_iyr(passport_record) -> bool:
    iyr = int(passport_record["iyr"])
    if not (2010 <= iyr <= 2020):
        print(f"iyr invalid: {iyr}")
        return False
    return True


def check_eyr(passport_record) -> bool:
    eyr = int(passport_record["eyr"])
    if not (2020 <= eyr <= 2030):
        print(f"eyr invalid: {eyr}")
        return False
    return True


HEIGHT_REGEX = re.compile("(\d+)(\w+)")


def check_hgt(passport_record) -> bool:
    match = re.match(HEIGHT_REGEX, passport_record["hgt"])
    if match is None:
        return False
    value, units = match.group(1, 2)
    if units == "in":
        if not (59 <= int(value) <= 76):
            print(f"hgt invalid: {value}{units}")
            return False
    elif units == "cm":
        if not (150 <= int(value) <= 193):
            print(f"hgt invalid: {value}{units}")
            return False
    else:
        return False

    return True


HAIR_COLOR_REGEX = re.compile("#[a-f0-9]{6}")


def check_hcl(passport_record) -> bool:
    match = re.match(HAIR_COLOR_REGEX, passport_record["hcl"])
    if match is None:
        print(f"hcl invalid: {passport_record['hcl']}")
        return False
    return True


def check_ecl(passport_record) -> bool:
    ecl = passport_record["ecl"]
    valid = ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    if not valid:
        print(f"ecl invalid: {ecl}")

    return valid


def check_pid(passport_record) -> bool:
    valid = len(passport_record["pid"]) == 9
    if not valid:
        print(f"pid invalid: {passport_record['pid']}")

    return valid


def passport_record_is_valid(passport_record: Dict[str, str]) -> bool:
    included_keys = set(passport_record.keys())
    if not required_keys.issubset(included_keys):
        return False

    checks = [
        check_birth_year,
        check_iyr,
        check_eyr,
        check_hgt,
        check_hcl,
        check_ecl,
        check_pid,
    ]
    if all(check(passport_record) for check in checks):
        return True

    return False


passport_records = [parse_record_from_line(line) for line in passport_batch]
valid_records = [
    record for record in passport_records if passport_record_is_valid(record)
]

print(len(valid_records))
