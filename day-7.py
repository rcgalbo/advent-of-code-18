from typing import Dict, Tuple, List, Set
import string   
smpl = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''

def parse_input(raw: str) -> List[Tuple[ str,str ]]:
    input_ = [l for l in raw.strip().split('\n')]
    data  = [(x[1],x[2]) for x in [[c for c in i if c.isupper()] for i in input_]]       
    return data

test = parse_input(smpl)
def unique(data: List[Tuple[str,str]]) -> List[str]:
    letters = set()
    for a,b in data:
        letters.add(a)
        letters.add(b)
    return list(letters)

with open('data/data-day7.txt') as f:
    data = parse_input(f.read())

def build_dependency(letters: List[str] , tups: List[Tuple[str,str]]):
    depends = {}
    for letter in letters:
        depends[letter] = []
        for tup in tups:
            a,b = tup
            if letter == b:
                depends[b] += a
            
    return depends

def subset(a,b):
    return set(a) <= set(b)

assert subset([],[]) == True

def get_has_sub(deps, order):
    availible = []
    for i,j in deps.items():
        if subset(j,order):
            availible.append(i)
    return availible

def order_dep(test):
    uni = unique(test)
    deps = build_dependency(uni, test)
    order = []
    while deps:
        availible = get_has_sub(deps, order)
        availible.sort()
        nxt = availible[0]
        if subset(deps[nxt],order):
            order.append(nxt)
            availible = availible[1:]
            del deps[nxt]
        
    return ''.join(order)
    
order_dep(test)
assert order_dep(test) == 'CABDFE'

print(order_dep(data))
            
# part two
lookup = {}
for i,j in enumerate(list(string.ascii_uppercase)):    
    lookup[j] = i+61

def get_has_time(deps, order, availible, n_workers):
    for i,j in deps.items():
        if subset(j,order):
            if i not in [i[0] for i in availible]:
                availible.append(( i,lookup[i] ))
    availible.sort(key = lambda x: x[0])
    return availible[0:n_workers+1]

def order_dep_time(test, n_workers):
    uni = unique(test)
    deps = build_dependency(uni, test)
    print(deps)
    order = []
    availible = []
    time = 0
    while deps:
        availible = get_has_time(deps, order, availible, n_workers)
        availible.sort(key=lambda x: x[1])
        print(order)
        while availible[0][1] > 0:
            time += 1
            availible = [(i[0],i[1] - 1) for i in availible]
            print(availible)
        nxt = availible[0][0]
        del deps[nxt]
        order.append(nxt)
        availible = availible[1:]
        
    print(''.join(order))
    return time

print(order_dep_time(data,5))