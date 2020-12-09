from typing import Set

with open("./input.txt") as f:
    answer_batch = f.read().split("\n\n")


def process_answer_batch(batch: str):
    people = [set(person) for person in batch.split()]
    questions = set.intersection(*people)
    return len(questions)


assert process_answer_batch("abc") == 3
assert process_answer_batch("a\nb\nc") == 0
assert process_answer_batch("ab\nac") == 1

total_questions = sum(process_answer_batch(batch) for batch in answer_batch)
print(total_questions)
