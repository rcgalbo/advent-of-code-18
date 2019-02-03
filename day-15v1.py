from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from tqdm import tqdm
import copy
import sys
# import simple graph for search

from graph_ex import Graph, dijkstra, shortest

# attempt 2
# don't use murky state

# state is less murky
# paradigmn very slow

# graph is faster
# graph state is murky when djikstra() called

from IPython.core.debugger import set_trace


class Cave(Dict):
    def __init__(self, cave_str: str):
        self.cave: Dict[Tuple[int, int], str] = self.parse_str(cave_str)
        self.turn: int = 0

    def __repr__(self):
        max_coord = max(self.cave.keys())
        st = []
        for i in range(max_coord[0]+1):
            st += '\n'
            for j in range(max_coord[1]+1):
                st += self[i, j]
        if self.turn == 0:
            return 'Initally:' + ''.join(st)
        return f'Turn: {self.turn}' + ''.join(st)

    def parse_str(self, cave_str: str) -> Dict[Tuple[int, int], str]:
        cave = {}
        for i, line in enumerate(cave_str.split('\n')):
            for j, char in enumerate(list(line.strip())):
                cave[(i, j)] = char
        return cave

    def get_empty(self) -> List[Tuple[int, int]]:
        return [c for c in self.cave.keys() if self[c] == '.']

    def __getitem__(self, key: Tuple[int, int]) -> str:
        return self.cave[key]

    def __setitem__(self, key: Tuple[int, int], value) -> str:
        self.cave[key] = value


class Unit:
    def __init__(self, pos: Tuple[int, int], kind: str):
        self.pos: Tuple[int, int] = pos
        self.kind: str = kind
        self.hp: int = 200
        self.opponent: Tuple[int, int] = (-1, -1)

    def __repr__(self):
        return f'{self.kind} {self.pos} hp: {self.hp} attacking: {self.opponent}\n'

    def free_adjacent(self, cave: 'Cave') -> bool:
        surround = adjacent(self.pos)
        for coord in surround:
            if cave[coord] == '.':
                return True
        return False

    def is_engaged(self):
        if self.opponent == (-1, -1):
            return False
        return True


def distance(c1: Tuple[int, int], c2: Tuple[int, int]) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def adjacent(coord: Tuple[int, int]):
    '''return coord ( up, down, right, left )'''
    i, j = coord
    return ((i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1))


def find_targets(kind: str, units: List['Unit']) -> List[Tuple[int, int]]:
    targets = []
    target_kind = {'G', 'E'} - {kind}
    for unit in units:
        if {unit.kind} == target_kind:
            targets.append(unit.pos)
    return targets


def path(start: Tuple[int, int],
         target: Tuple[int, int],
         cave: 'Cave') -> Optional[List[Tuple[int, int, int]]]:
    i = 0

    start_surround = [c for c in adjacent(start) if cave[c] == '.']
    free_spaces = [c for c in cave.cave.keys() if cave[c] == '.']

    paths = [target + (i,)]
    found = []

    while i < len(free_spaces):
        coords = [p[0:2] for p in paths if p[2] == i]
        all_coords = [p[0:2] for p in paths]
        i += 1

        if len(coords) == 0:
            i += 1

        for point in coords:
            if point in start_surround and point not in [f[0:2] for f in found]:
                found.append(point + (i,))

        for point in coords:
            adjacents = [adj for adj
                         in adjacent(point)
                         if cave[adj] == '.' and
                         adj not in all_coords]

            for coord in adjacents:

                if coord in start_surround and coord not in [f[0:2] for f in found]:
                    found.append(coord + (i,))

                    if len(found) == len(start_surround):
                        return found

                if coord not in all_coords:
                    paths.append(coord + (i,))

    if len(found) > 0:
        return found


def path2(start: Tuple[int, int],
          target: Tuple[int, int],
          cave: 'Cave',
          graph: 'Graph') -> Optional[List[Tuple[int, int, int]]]:

    i = 0

    start_surround = [c for c in adjacent(start) if cave[c] == '.']
    free_spaces = [c for c in cave.cave.keys() if cave[c] == '.']

    # filter with graph search
    start_surround = [
        c for c in start_surround if graph.isReachable(c, target)]
    if not start_surround:
        return []

    paths = [target + (i,)]
    found = []

    while i < len(free_spaces):
        coords = [p[0:2] for p in paths if p[2] == i]
        all_coords = [p[0:2] for p in paths]
        i += 1

        if len(coords) == 0:
            i += 1

        for point in coords:
            if point in start_surround and point not in [f[0:2] for f in found]:
                found.append(point + (i,))

        for point in coords:
            adjacents = [adj for adj
                         in adjacent(point)
                         if cave[adj] == '.' and
                         adj not in all_coords]

            for coord in adjacents:

                if coord in start_surround and coord not in [f[0:2] for f in found]:
                    found.append(coord + (i,))

                    if len(found) == len(start_surround):
                        return found

                if coord not in all_coords:
                    paths.append(coord + (i,))

    if len(found) > 0:
        return found


def pathfinder(unit: 'Unit',
               units: List['Unit'],
               cave: 'Cave') -> Optional[List[Tuple[int, int, int]]]:

    unit_moves = []
    targets = find_targets(unit.kind, units)
    target_adjacents = [pos for target in targets
                        for pos in adjacent(target)
                        if cave[pos] == '.']

    if not target_adjacents:
        return []

    for target in target_adjacents:
        p = path(unit.pos, target, cave)
        if p:
            unit_moves.extend(p)

    if not unit_moves:
        return []

    unit_moves.sort(key=lambda x: (x[2], x[0], x[1]))

    return unit_moves[0]


def path3(start: Tuple[int, int],
          target: Tuple[int, int],
          graph: 'Graph') -> Optional[List[Tuple[int, int, int]]]:
    
    tv = graph.get_vertex(target)
    path = [tv.get_id()]
    shortest(tv, path)

    if start in path:
        return path


def pathfinder2(unit: 'Unit',
                units: List['Unit'],
                cave: 'Cave') -> Optional[List[Tuple[int, int, int]]]:

    unit_moves = []
    empty = cave.get_empty()

    start_adjacents = [pos for pos in adjacent(unit.pos) if pos in empty]

    targets = find_targets(unit.kind, units)
    target_adjacents = [pos for target in targets
                        for pos in adjacent(target)
                        if pos in empty]

    if not target_adjacents:
        return []
            
    # check if any moves immediately availible
    for target in target_adjacents:
        if target in start_adjacents:
            move = target + (0, )
            unit_moves.append(move)
        
    if unit_moves:
        unit_moves.sort(key=lambda x: (x[0], x[1]))
        return unit_moves[0]

    g = Graph.build(empty)
    # set_trace()

    for start in start_adjacents:
        # compute  the distance to targets
        dijkstra(g, g.get_vertex(start))
        for target in target_adjacents:
            p = path3(start, target, g)
            if p:
                move = start + (len(p), )
                unit_moves.append(move)
        # reset graph state
        g.reset()

    if not unit_moves:
        return []

    unit_moves.sort(key=lambda x: (x[2], x[0], x[1]))

    return unit_moves[0]


def make_units(cave: 'Cave') -> List['Unit']:
    units = []
    for loc in cave.cave.keys():
        if cave[loc] in ['G', 'E']:
            units.append(Unit(loc, cave[loc]))
    return units


def get_unit(loc: Tuple[int, int], units: List['Unit']) -> Tuple[int, 'Unit']:
    '''takes location and list of unit returns index and unit'''
    for i, unit in enumerate(units):
        if unit.pos == loc:
            return i, unit


def get_weakest(coords: List[Tuple[int, int]],
                units: List['Units']) -> Tuple[int, int]:
    potentials = [u for u in units if u.pos in coords if u.hp >= 0]
    potentials.sort(key=lambda x: (x.hp, x.pos[0], x.pos[1]))
    if not potentials:
        return (-1, -1)
    return potentials[0].pos

def total_hp(units):
    return sum(u.hp for hp in units if u.hp > 0)

def engaged(unit: 'Unit', units: List['Unit'], cave: 'Cave') -> 'Unit':

    if not unit.is_engaged():
        target_kind = {'G', 'E'} - {unit.kind}
        surround = adjacent(unit.pos)
        potentials = []

        # find surround with enemy
        for pos in surround:
            if {cave[pos]} == target_kind:
                potentials.append(pos)
        # if surround with enemy, get weakest
        if potentials:
            unit.opponent = get_weakest(potentials, units)

    if unit.is_engaged():
        # if enemy died
        target_kind = {'G', 'E'} - {unit.kind}
        surround_coord = adjacent(unit.pos)
        not_surround = [{cave[coord]} !=
                        target_kind for coord in surround_coord]
        # check surround for another attack
        if all(not_surround):
            unit.opponent = (-1, -1)
        else:
            potentials = [pos for pos
                          in surround_coord
                          if {cave[pos]} == target_kind]
            new_oppo = get_weakest(potentials, units)
            unit.opponent = new_oppo

    return unit


def break_game(units, cave):
    hps = sum(u.hp for u in units)
    print(f'turn: {cave.turn} points: {hps}')
    print(f'outcome: {cave.turn * hps}')
    raise ValueError('No more enemies left')


def run(cave: 'Cave', units: List['Unit']) -> (List['Cave'], List['Unit']):
    if cave.turn == 0:
        print(cave)
        print(units)

    kinds = {u.kind for u in units}
    if len(kinds) < 2:
        print('full turn end')
        break_game(units, cave)

    else:

        # update position order
        units.sort(key=lambda x: (x.pos[0], x.pos[1]))

        # iterate over units
        # unit turn start
        num_units = len(units)
        for i in tqdm(range(num_units)):

            # overflow from removing dead units
            if i >= len(units):
                continue

            # check if fighting at beginning
            unit = engaged(units[i], units, cave)

            # if not fighting move
            if unit.opponent == (-1, -1):
                next_move_tuple = pathfinder2(unit, units, cave)
                next_move = next_move_tuple[0:2]
                if len(next_move) > 0:
                    cave[unit.pos] = '.'
                    unit.pos = next_move
                    cave[unit.pos] = unit.kind

                # check if fighting after moving
                unit = engaged(unit, units, cave)

            # if fighting attack
            if unit.opponent != (-1, -1):

                # check if fighting weakest adjacent unit
                if unit.hp > 0:
                    j, opponent = get_unit(unit.opponent, units)
                    opponent.hp -= 3
                    units[j] = opponent

                # check to see if game should continue

                if opponent.hp < 0:
                    kinds = {u.kind for i, u in enumerate(units) if i != j}
                    ind = units.index(opponent)
                    from_end = len(units) - 1 - ind

                    if len(kinds) < 2 and from_end != 1:
                        units.pop(j)
                        cave[opponent.pos] = '.'
                        print('partial turn end')
                        break_game(units, cave)

            units[i] = unit

    # removing dead units
    for j, unit in enumerate(units):
        if unit.hp < 0:
            cave[unit.pos] = '.'
            units.pop(j)

    cave.turn += 1
    print(cave)

    units.sort(key=lambda x: x.pos[0])
    print(units)

    return cave, units


if __name__ == '__main__':

    ex1 = """#######
    #E..G.# 
    #...#.# 
    #.G.#G# 
    #######"""

    ex2 = """#######
    #.E...#
    #.....#
    #...G.#
    #######"""

    ex3 = """#########
    #G..G..G#
    #.......#
    #.......#
    #G..E..G#
    #.......#
    #.......#
    #G..G..G#
    #########"""

    ex4 = """#######   
    #.G...#
    #...EG#
    #.#.#G#
    #..G#E#
    #.....#
    #######"""
    # 47, 590
    # outcome: 27730

    ex5 = """#######
    #G..#E#
    #E#E.E#
    #G.##.#
    #...#E#
    #...E.#
    #######"""
    # 37, 982
    # outcome: 36334

    ex6 = """#######
    #E..EG#
    #.#G.E#
    #E.##E#
    #G..#.#
    #..E#.#
    #######"""
    # 46, 859
    # outcome: 39514

    ex7 = """#######
    #E.G#.#
    #.#G..#
    #G.#.G#
    #G..#.#
    #...E.#
    #######"""
    # 35, 793
    # outcome: 27755

    ex8 = """#######
    #.E...#
    #.#..G#
    #.###.#
    #E#G#G#
    #...#G#
    #######"""
    # 54,536
    # outcome: 28944

    ex9 = """#########
    #G......#
    #.E.#...#
    #..##..G#
    #...##..#
    #...#...#
    #.G...G.#
    #.....G.#
    #########"""
    # 20, 937
    # outcome: 18740

    c = Cave(ex1)
    u = make_units(c)

    c = Cave(ex2)
    u = make_units(c)

    c = Cave(ex3)
    u = make_units(c)

    # ---------------

    c = Cave(ex4)
    u = make_units(c)

    c = Cave(ex5)
    u = make_units(c)

    c = Cave(ex6)
    u = make_units(c)

    c = Cave(ex7)
    u = make_units(c)

    c = Cave(ex8)
    u = make_units(c)

    c = Cave(ex9)
    u = make_units(c)

    # part 1
    # with open('data/data-day15.txt') as f:
    #     c = Cave(f.read())
    # u = make_units(c)

    while True:
        c, u = run(c, u)
