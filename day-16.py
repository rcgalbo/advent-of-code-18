from typing import NamedTuple, List, Dict
from collections import defaultdict
from itertools import repeat
from functools import partial
from copy import copy


class Sample(NamedTuple):
    before: List[int]
    after: List[int]
    instruction: List[int]

# addition
def addr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] + before[b]
    return True if before == smp.after else False, before

def addi(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] + b
    return True if before == smp.after else False, before

def mulr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] * before[b]
    return True if before == smp.after else False, before

def muli(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] * b
    return True if before == smp.after else False, before

def banr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] & before[b]
    return True if before == smp.after else False, before

def bani(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] & b
    return True if before == smp.after else False, before

def borr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] | before[b]
    return True if before == smp.after else False, before


def bori(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a] | b
    return True if before == smp.after else False, before

def setr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = before[a]
    return True if before == smp.after else False, before

def seti(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = a
    return True if before == smp.after else False, before

def gtir(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if a > before[b] else 0
    return True if before == smp.after else False, before

def gtri(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if before[a] > b else 0
    return True if before == smp.after else False, before

def gtrr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if before[a] > before[b] else 0
    return True if before == smp.after else False, before

def eqir(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if a == before[b] else 0
    return True if before == smp.after else False, before

def eqri(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if before[a] == b else 0
    return True if before == smp.after else False, before

def eqrr(smp: 'Sample') -> bool:
    before = smp.before.copy()
    a, b, c = smp.instruction[1:]
    before[c] = 1 if before[a] == before[b] else 0
    return True if before == smp.after else False, before

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

# assert mulr(test) == True
# assert seti(test) == True
# assert addi(test) == True

# # part 1 samples

# # apply all functions to the input count # >= 3
# # https://stackoverflow.com/questions/11736407/apply-list-of-functions-on-an-object-in-python
# def apply(f, a): # just currying
#     return f(a)
# assert sum(map(partial(apply, a=test), ops)) == 3

with open('data/data-day16.txt') as f:
    samples, test_data = f.read().split('\n\n\n')
samples = read_samples(samples)

# number_match = [sum(map(partial(apply, a=smp), ops)) for smp in samples]
# print(sum(n >= 3 for n in number_match))

# part 2 test

test_data = [
    [int(i) for i in test.split(' ') if i.isdigit()] for test in test_data.split('\n')
][1:]

# create mapping {num: function}
def match_functions(samples, ops):
    final = {}
    while True:
        matches = defaultdict(set)
        for smp in samples:
            id = smp.instruction[0]
            for f in ops:
                if f(smp)[0] == True and id not in final.keys() and f not in final.values():
                    matches[id].add(f)

        for id in matches:
            if len(matches[id]) == 1:
                final[id] = matches[id].pop()

        if len(matches.keys()) == 0:
            return final

mapping = match_functions(samples, ops)

# apply
before = test_data[0]
instruction = test_data[1]
fn = 1 # seti
after = before[0:instruction[]
s = Sample(before, before , instruction)
for t in test_data[2:]:
    fn = s.instruction
    f = mapping[fn]
    s = Sample(t, f(s)[1], f(s)[1])