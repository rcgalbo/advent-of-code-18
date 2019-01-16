from typing import NamedTuple, Tuple, List
from matplotlib import pyplot as plt
import re, time

# sample data
with open('data/data-day10smp.txt') as f:
    lines = [l for l in f.read().strip().split('\n')]

reg = 'position=<(.*), (.*)> velocity=<(.*), (.*)>'
smp = [c for c in (re.match(reg, line).groups() for line in lines)]
coords = [(int(i[0]),int(i[1]),int(i[2]),int(i[3])) for i in smp]

class Point(NamedTuple):
    coord: Tuple[int]
    momentum: Tuple[int]

    @staticmethod
    def build(coord: Tuple[int]) -> 'Point':
        return Point((coord[0],coord[1]), (coord[2],coord[3]))
    
def get_bound(p: List['Point']) -> Tuple[int]:
    max_x = max(a.coord[0] for a in p)
    max_y = max(a.coord[1] for a in p)
    min_x = min(a.coord[0] for a in p)
    min_y = min(a.coord[1] for a in p)

    return min_x, min_y, max_x, max_y 

def update(p: Point):
    x = p.coord[0] + p.momentum[0]
    y = p.coord[1]  + p.momentum[1]
    return Point.build((x,y, *p.momentum))

def unupdate(p: Point):
    x = p.coord[0] - p.momentum[0]
    y = p.coord[1]  - p.momentum[1]
    return Point.build((x,y, *p.momentum))
        

def plot(points):
    x = [p.coord[0] for p in points]
    y = [p.coord[1] for p in points]
    plt.xlim((-1000,1000))
    plt.ylim((-1000,1000))
    plt.scatter(x,y)


def update_plot_500(c, ps):
    for i in range(500):
        ps = [update(p) for p in ps]
    plt.clf()
    plot(ps)
    return c+500, ps

def update_plot_50(c,ps):
    for i in range(50):
        ps = [update(p) for p in ps]
    plt.clf()
    plot(ps)
    return c+50, ps

def update_plot(c, ps):
    ps = [update(p) for p in ps]
    plt.clf()
    plot(ps)
    return c+1, ps

def unupdate_plot(c, ps):
    ps = [unupdate(p) for p in ps]
    plt.clf()
    plot(ps)
    return c-1, ps


# real data
with open('data/data-day10.txt') as f:
    lines = [l for l in f.read().strip().split('\n')]

reg = 'position=<(.*), (.*)> velocity=<(.*), (.*)>'
smp = [c for c in (re.match(reg, line).groups() for line in lines)]
coords = [(int(i[0]),int(i[1]),int(i[2]),int(i[3])) for i in smp]
points = [Point.build(coord) for coord in coords]
ps = [update(p) for p in points]

