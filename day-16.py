from typing import NamedTuple, List, Dict, Callable
from collections import defaultdict
from itertools import repeat
from functools import partial
from copy import copy


class Sample(NamedTuple):
    before: List[int]
    after: List[int]
    instruction: List[int]


# addition
def addr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] + before[b]
    return before


def addi(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] + b
    return before


def mulr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] * before[b]
    return before


def muli(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] * b
    return before


def banr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] & before[b]
    return before


def bani(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] & b
    return before


def borr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] | before[b]
    return before


def bori(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a] | b
    return before


def setr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = before[a]
    return before


def seti(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = a
    return before


def gtir(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if a > before[b] else 0
    return before


def gtri(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if before[a] > b else 0
    return before


def gtrr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if before[a] > before[b] else 0
    return before


def eqir(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if a == before[b] else 0
    return before


def eqri(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if before[a] == b else 0
    return before


def eqrr(before: List[int], instruction: List[int]) -> List[int]:
    before = copy(before)
    a, b, c = instruction[1:]
    before[c] = 1 if before[a] == before[b] else 0
    return before


ops = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


def read_samples(sample_str: str) -> List['Sample']:
    samples = []
    sample_list = [smp.strip() for smp in sample_str.split('\n\n')]
    for sample in sample_list:
        before, after, instruction = [], [], []
        lines = sample.split('\n')
        for line in lines:
            # from pdb import set_trace;set_trace()
            line = line.replace(',', '', 5).replace('[', '').replace(']', '')
            chars = line.split(' ')
            sample_list = [int(char) for char in chars if char.isdigit()]
            if 'Before' in line:
                before = sample_list
            elif 'After' in line:
                after = sample_list
            else:
                instruction = sample_list
        samples.append(Sample(before, after, instruction))
    return samples


test = Sample([3, 2, 1, 1], [3, 2, 2, 1], [9, 2, 1, 2])
assert mulr(test.before, test.instruction) == test.after
assert seti(test.before, test.instruction) == test.after
assert addi(test.before, test.instruction) == test.after

# part 1 samples
# apply all functions to the input count # >= 3
# https://stackoverflow.com/questions/11736407/apply-list-of-functions-on-an-object-in-python
def apply(f: Callable, a: 'Sample') -> bool:  # kinda currying
    return f(a.before, a.instruction) == a.after


assert sum(map(partial(apply, a=test), ops)) == 3

with open('data/data-day16.txt') as f:
    samples, test_data = f.read().split('\n\n\n')

samples = read_samples(samples)
number_match = [sum(map(partial(apply, a=smp), ops)) for smp in samples]
print(sum(n >= 3 for n in number_match))

# part 2 test
test_data = [
    [int(i) for i in test.split(' ') if i.isdigit()]
    for test in test_data.strip().split('\n')
]


def match_functions(
    samples: List['Sample'], ops: List[Callable]
) -> Dict[int, Callable]:
    """create a mapping from operation number to function"""
    final = {}
    while True:
        matches = defaultdict(set)
        for smp in samples:
            id = smp.instruction[0]
            for f in ops:
                if (
                    f(smp.before, smp.instruction) == smp.after
                    and id not in final.keys()
                    and f not in final.values()
                ):
                    matches[id].add(f)

        for id in matches:
            if len(matches[id]) == 1:
                final[id] = matches[id].pop()

        if len(matches.keys()) == 0:
            return final


mapping = match_functions(samples, ops)

# apply
first = [0, 0, 0, 0]
inst = test_data[0]
f = mapping[inst[0]]
out = f(first, inst)

for inst in test_data[1:]:
    f = mapping[inst[0]]
    out = f(out, inst)

print(out[0])
