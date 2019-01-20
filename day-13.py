from typing import List, Tuple, NamedTuple
from itertools import cycle, combinations 

example = r"""
/->-\        
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

def read_track(instring: str) -> List[str]:
    return [list(l) for l in instring.split('\n')]

ex_track = read_track(example)[1:]

with open('data/data-day13.txt') as f:
    track = read_track(f.read())

def print_track(track: List[str]) -> None:
    print('\n'.join(''.join(t) for t in track))

class Cart():
    def __init__(self, loc, dir, track):
        self.loc = loc
        self.dir = dir
        self.turn = cycle(['left', 'straight', 'right'])
        self.last_track = self.set_last()

    def __repr__(self):
        return f'{self.dir},{self.loc}'

    def set_last(self):
        if self.dir == 'v' or self.dir == '^':
            last_track = '|'
        elif self.dir == '>' or self.dir == '<':
            last_track = '-'
        return last_track


def find_carts(track: List[str]) -> List['Cart']:
    carts = []
    for y, row in enumerate(track):
        for x, char in enumerate(row):
            if char in {'>','<','^','v'}:
                carts.append(Cart((x,y), char, track))

    return carts


def turn(cart: 'Cart') -> None:
    new_dir = next(cart.turn)
    if cart.dir == '^':
        if new_dir == 'left':
            cart.dir = '<'
        if new_dir == 'right':
            cart.dir = '>'
    elif cart.dir == 'v':
        if new_dir == 'left':
            cart.dir = '>'
        if new_dir == 'right':
            cart.dir = '<'
    elif cart.dir == '>':
        if new_dir == 'left':
            cart.dir = '^'
        if new_dir == 'right':
            cart.dir = 'v'
    elif cart.dir == '<':
        if new_dir == 'left':
            cart.dir = 'v'
        if new_dir == 'right':
            cart.dir = '^'

def get_next(loc: Tuple[int, int], dir: str) -> Tuple[int, int]:
    if dir == '^':
        loc = (loc[0], loc[1]-1)
    elif dir == 'v':
        loc = (loc[0], loc[1]+1)
    elif dir == '>':
        loc = (loc[0]+1,loc[1])
    elif dir == '<':
        loc = (loc[0]-1, loc[1])
    return loc

def check_collisions(track: List[str], carts: List[str]):
    carts.sort(key = lambda x: (x.loc[1],x.loc[0]))
    collisions = []
    for a, b in combinations(carts,2):
        if a.loc == b.loc:
            collisions.append(a.loc)
            track[a.loc[1]][a.loc[0]] = a.last_track
            print(f'collision @ {collisions[-1]}')

    carts = [c for c in carts if c.loc not in collisions]
    return track, carts

def move(track, carts):
    for cart in carts:
        c_x, c_y = cart.loc
        track[c_y][c_x] = cart.last_track

        n_x, n_y = get_next(cart.loc, cart.dir)
        next_track = track[n_y][n_x]
        cart.loc = (n_x,n_y)

        if next_track == '+':
            turn(cart)
        if next_track == '\\':
            if cart.dir == '^':
                cart.dir = '<'
            elif cart.dir == 'v':
                cart.dir = '>'
            elif cart.dir == '>':
                cart.dir = 'v'
            elif cart.dir == '<':
                cart.dir = '^'
        if next_track == '/':
            if cart.dir == '^':
                cart.dir = '>'
            elif cart.dir == 'v':
                cart.dir = '<'
            elif cart.dir == '>':
                cart.dir = '^'
            elif cart.dir == '<':
                cart.dir = 'v'
        
        cart.last_track = next_track
        track[n_y][n_x] = cart.dir

    return track

# test
print('part 1 test')
ex_carts = find_carts(ex_track)
num_carts = len(ex_carts)
while len(ex_carts) == num_carts:
    ex_track = move(ex_track,ex_carts)
    ex_track, ex_carts = check_collisions(ex_track, ex_carts)
print('\n')

carts = find_carts(track)

# part 1
print('part 1')
cart_len = len(carts)
while len(carts) >= cart_len:
    track = move(track, carts)
    track, carts = check_collisions(track, carts)
print('\n')

# test: part 2
ex2_track = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""
print('part 2 test')
ex2_track = read_track(ex2_track)[1:]
ex2_carts = find_carts(ex2_track)
while len(ex2_carts) > 1:
    ex2_track = move(ex2_track, ex2_carts)
    ex2_track, ex2_carts = check_collisions(ex2_track, ex2_carts)
print(ex2_carts)
print('\n')

# part 2
print('part 2')
with open('data/data-day13.txt') as f:
    track2 = read_track(f.read())
carts2 = find_carts(track2)
while len(carts2) > 1:
    track2 = move(track2, carts2)
    track2, carts2 = check_collisions(track2, carts2)
print(carts2)