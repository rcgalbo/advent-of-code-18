'''
day-3

part 1:
goal to count # of locations with overlapping claims
- get cloth size
- add claims on cloth
- find # locations where claims > 1

#123 @ 3,2: 5x4 means 
# claim ID 123 
# 3 inches from the left edge 
# 2 inches from the top edge 
# 5 inches wide 
# 4 inches tall

input:
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

visual:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

'''

from typing import Tuple, List
import numpy as np


def parse_claim(claim: str):
    claim = claim.strip().split(' ')
    id = claim[0]
    coords = tuple( claim[2].split(',') )
    x = coords[0]
    y = coords[1].replace(':','')
    dimensions = tuple( claim[3].split('x') )
    w = dimensions[0]
    h = dimensions[1]

    return tuple(int(i) for i in [ x,y,w,h ])

assert parse_claim("#123 @ 5,4: 2x4") == (5,4,2,4)

def get_max_dimension(claims):
    max_x = 0
    max_y = 0
    for claim in claims:
        dim = ( claim[0]+claim[2], claim[1]+ claim[3] )
        if dim[0] > max_x:
            max_x = dim[0]
        if dim[1] > max_y:
            max_y = dim[1]

    return (max_x,max_y)

assert get_max_dimension([ (5,4,2,4) ]) == (7,8)

def make_cloth(shape: Tuple):
    return np.zeros(shape,dtype=np.int)

assert make_cloth((4,5)).shape == (4,5)

class Claim:
    def __init__(self,claim):
        self.x = claim[0]
        self.y = claim[1]
        self.to_x = claim[0] + claim[2]
        self.to_y = claim[1] + claim[3]
        self.size = claim[2]*claim[3]


class Cloth:
    def __init__(self,claims):
        self.claims = [parse_claim(claim) for claim in data]
        self.size = get_max_dimension(self.claims)
        self.cloth =  make_cloth(self.size)
    
    def draw_claim(self,claim):
        x = claim[0]
        y = claim[1]
        to_x = claim[0] + claim[2]
        to_y = claim[1] + claim[3]
        self.cloth[x:to_x,y:to_y] += 1
    
def find_free(is_1, claim):
    c = Claim(claim)        
    if np.sum(is_1[c.x:c.to_x,c.y:c.to_y]) == c.size:
        return f'{c.x} {c.y} alone'

if __name__ == "__main__":
    with open('data/data-day3.txt') as f:
        data = [c.strip('\n') for c in f.readlines()]

    cloth = Cloth(data)          
    # add claims to the cloth
    for claim in cloth.claims:
        cloth.draw_claim(claim)
    
    c = cloth.cloth

    print(f'{np.sum(c > 1)}: squares overlap')

    is_1 = (c == 1)
    i=0
    for claim in cloth.claims:
        i += 1
        if find_free(is_1,claim):
            print(f'id# { i } has no overlap')
        

