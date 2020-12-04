from typing import Dict

required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

with open('./input.txt') as f:
	passport_batch = f.read().split("\n\n")

def parse_record_from_line(batch_line: str) -> Dict[str, str]:
	key_pairs = batch_line.split()
	passport_record = {}
	for key_pair in key_pairs:
		key, value = key_pair.split(':')
		passport_record[key] = value
	return passport_record

def passport_record_is_valid(passport_record: Dict[str, str]) -> bool:
	included_keys = set(passport_record.keys())
	return required_keys.issubset(included_keys)

passport_records = [parse_record_from_line(line) for line in passport_batch]
valid_records = [record for record in passport_records if passport_record_is_valid(record)]

print(len(valid_records))