"""

"""
from typing import Tuple, Iterable

from collections import Counter
import string
import itertools

smp = 'dabAcCaCBAcCcaDA'

def react(a: str, b: str) -> bool:
    if a.casefold() == b.casefold() and a != b:
        return True
    else: 
        return False

assert react('a','A') == True
assert react('A', 'A') == False
assert react('A','b') == False
assert react('a','b') == False

def pairwise(iter: str) -> Iterable:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iter)
    next(b, None)
    return zip(a, b)   

def hasReaction(polymer: str) -> bool:
    iter = pairwise(polymer)
    for a,b in iter:
        if react(a,b):
            return True
    return False

def reaction(polymer: str) -> str:
    new = ''
    iter = pairwise(polymer)
    for a,b in iter:
        if react(a,b):
            try:
                next(iter)
            except:
                StopIteration
        else:
            new += a
    new += b
    return new

assert reaction(smp) == 'dabAaCBAcaDA'

new = smp
while hasReaction(new):
    new = reaction(new)
assert new == 'dabCBAcaDA'

def remove_type(polymer: str, type: str) -> str:
    new = ''
    for p in polymer:
        if p.casefold() == type.casefold():
            pass
        else: new += p
    return new

assert remove_type(smp, 'a') == 'dbcCCBcCcD'
assert remove_type(smp, 'b') == 'daAcCaCAcCcaDA'

# --- REACTOR ---
with open('data/data-day5.txt') as f:
    txt = f.read()

def run_experiment(polymer: str) -> int:
    tst = polymer
    while hasReaction(tst):
        tst = reaction(tst)
    return len(tst)


def run_removed(polymer: str) -> dict:
    c = {}
    for t in list( string.ascii_lowercase ):
        tst = remove_type(polymer, t)
        c[t] = run_experiment(tst)
    return c

c = run_removed(txt)
print(c)