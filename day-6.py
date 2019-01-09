# size of largest area that isn't infinite
# is infinite if contains any coordinate on border
# area has (0,i), (i,0) (max(k),i), (i, max(k))

# solution
# add ids
# for location in array, find nearest point, make index
# remove index on edges
# for index not on edge, count indexes return most common
from typing import Tuple, List
from collections import Counter
import numpy as np

smp = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

def get_dim(smp: str) -> Tuple[List[int], Tuple[int,int]]:
    el = [(int(i),int(j)) for i,j in (s.split(',')
                          for s in smp.strip().split('\n'))]
    min_x = min([i[0] for i in el])
    min_y = min([i[1] for i in el])
    max_x = max([i[0] for i in el])
    max_y = max([i[1] for i in el])
    return (el, (min_x,min_y, max_x, max_y))

assert get_dim(smp)[1]  == (1,1,8,9)

def build_grid(points, x, y) -> np.array:
    arr = np.zeros((x+1,y+1),dtype = int)
    for i, p in points:
        arr[p] = i
    return arr


def city_distance(p1: Tuple[int,int], p2: Tuple[int,int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

assert city_distance((1,1),(2,2)) == 2
assert city_distance((1,1),(1,1)) == 0

def find_infinite(grid: np.array) -> set:
    max_x, max_y = grid.shape
    top = set(grid[0,:])
    left = set(grid[:,0])
    bottom = set(grid[max_x-1,:])
    right = set(grid[:,max_y-1])
    return top | left | bottom | right  

def assign_points(grid: np.array, points: List[Tuple[int, Tuple[int,int]]]) -> np.array:
    grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            dist = [ (t,city_distance((i,j),p)) for t,p in points ]
            ordered = sorted(dist,key = lambda x: x[1])
            if grid[i,j] != ordered[0][0]:
                if ordered[0][1] == ordered[1][1]:
                    grid[i,j] = -1 
                else:
                    grid[i,j] += ordered[0][0]
    return grid

def assign_points_range(grid: np.array, points: List[Tuple[int, Tuple[int,int]]], max: int)-> np.array:
    grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            dist = sum([city_distance((i,j),p) for t,p in points])
            if dist < 10000:
                grid[i,j] = 1
    return grid


class Grid():
    def __init__(self, data: str):
        coords, (min_x, min_y, max_x, max_y) = get_dim(data)
        self.points = [(i+1, coord) for i,coord in enumerate(coords)]
        self.g = build_grid(self.points,max_x,max_y)
    
    def max_finite(self) -> Counter:
        grid_min = assign_points(self.g,self.points)
        infinite = find_infinite(grid_min)
        finite_values = [p[0] for p in self.points if p[0] not in infinite]
        inner = []
        for f in finite_values:
            inner += list(grid_min[grid_min == f])
        return Counter(inner).most_common(1)
    
    def in_range(self, max: int) -> int:
        grid_range = assign_points_range(self.g,self.points,max)
        return len(grid_range[grid_range == 1])
 
g = Grid(smp)
assert g.g.shape == (9,10)
assert find_infinite(g.g) == {0,3,6}

with open('data/data-day6.txt') as f:
    filestr = f.read()

# part 1
t = Grid(filestr)
print(t.max_finite())
# part 2
print(t.in_range(10000))
