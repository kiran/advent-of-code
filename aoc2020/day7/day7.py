from __future__ import annotations
import attr
from typing import Set, Dict


@attr.s(auto_attribs=True)
class Rule:
    color: str
    # mapping from color to number
    contents: Dict[str, int]

    @classmethod
    def from_string(cls, stmt: str) -> Rule:
        # todo: use a regex instead
        stmt = stmt.replace("bags", "").replace("bag", "").replace(".", "")
        color, contents_str = stmt.split(" contain ")

        contents: Dict[str, int] = {}

        if contents_str != "no other ":
            for bag_spec in contents_str.split(","):
                num, bag_color = bag_spec.strip().split(" ", 1)
                contents[bag_color] = int(num)

        return cls(color.strip(), contents)


assert Rule.from_string("dotted black bags contain no other bags.").contents == {}

rules_dict: Dict[str, Rule] = {}


with open("./input.txt") as f:
    input_lines = f.read().splitlines()

for line in input_lines:
    rule = Rule.from_string(line)
    rules_dict[rule.color] = rule


def can_contain_bag(inner_bag: str, outer_bag: str) -> bool:
    outer_bag_rule = rules_dict[outer_bag]

    # either it can directly contain the bag
    if inner_bag in outer_bag_rule.contents:
        return True

    # or one of its bags can contain it
    return any(
        can_contain_bag(inner_bag, sub_outer_bag)
        for sub_outer_bag in outer_bag_rule.contents.keys()
    )


# assert can_contain_bag("shiny gold", "bright white")
# assert can_contain_bag("shiny gold", "dark orange")


def bags_can_contain(inner_bag: str) -> Set[str]:
    # todo: DP this
    can_contain = set()
    for outer_bag in rules_dict.keys():
        if can_contain_bag(inner_bag, outer_bag):
            can_contain.add(outer_bag)

    return can_contain


def number_bags_contained(bag_color: str) -> int:
    num_contained = 0

    bag_rule = rules_dict[bag_color]
    for sub_bag, number in bag_rule.contents.items():
        num_contained += number * (1 + number_bags_contained(sub_bag))

    return num_contained


# assert number_bags_contained("faded blue") == 0
# assert number_bags_contained("dark olive") == 7
# assert number_bags_contained("shiny gold") == 32

# assert number_bags_contained("shiny gold") == 126

print(number_bags_contained("shiny gold"))

# print(len(bags_can_contain("shiny gold")))
