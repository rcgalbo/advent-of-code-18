from typing import Tuple, List, Set, Dict
import copy

# reading order: top-bottom -> left right

# rounds: move + atack

# move:
ex1="""####### 
#E..G.# 
#...#.# 
#.G.#G# 
#######""" 

#######       #######       #######       #######
#?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
#.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
#E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
#######       #######       #######       #######

# targets (all enemies)
# in range (open adjacent square)
# reachable (has path to open adjacent square)
# choice (shortest path -> reading order)
# step - square along shortest path (reading order ties)

# attack
# 3 attack power, 20 hp

# outcome: n_turns * sum of remaining hp

EX = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""

def top_reading_order(struct: Dict[Tuple[int, int], int]) -> Tuple[int, int]:
    if len(struct) == 0:
        return None
    shortest = min(struct.values())
    struct = {k: v for k, v in struct.items() if v == shortest}
    struct = sorted(struct.items(), key = lambda x: (x[0][0],x[0][1]))
    return struct[0][0]

def distance(a: Tuple[int, int],b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def print_target(a: List) -> None:
    print('\n'.join(''.join(str(i) for i in row )for row in a))

def get_empty_surround(a: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
    y, x = a

    empty = []
    # search up, down, left, right for empty space
    for s_y, s_x in [(y+1,x),(y-1,x),(y,x-1),(y,x+1)]:
        if board[s_y][s_x] == '.':
            empty.append((s_y,s_x))

    return empty 

def get_surround(a: Tuple[int, int], board: 'Board') -> List[Tuple[int, int]]:
    y, x = a

    surround = []
    # search up, down, left, right for empty space
    for s_y, s_x in [(y+1,x),(y-1,x),(y,x-1),(y,x+1)]:
        surround.append((s_y,s_x))

    return surround 

class Character:
    def __init__(self, type: str, pos: Tuple[int, int], hp: int = 200):
        self.type = type
        self.pos = pos
        self.hp = hp
        self.fight = None

    def __repr__(self):
        return f'{self.type} @ {self.pos}: HP={self.hp}'
    
    def target(self, board: 'Board')-> Tuple[int, int]:
        target = {}
        enemies = [char for char in board.characters if char.type != self.type]
        empty_attack = []
        for enemy in enemies:
            empty_attack.extend(get_empty_surround(enemy.pos, board))
        
        if len(empty_attack) > 0:
            for space in empty_attack: 
                if board.check_path(self.pos, space):
                    target[space] = distance(self.pos, space)
        
        return top_reading_order(target)
    
    def is_engaged(self, board):
        y, x = self.pos
        for s_y, s_x in [(y+1,x),(y-1,x),(y,x-1),(y,x+1)]:
                if {board[s_y][s_x]} == board.classes.difference({self.type}):
                    return True
        else:
            return False

    def is_surrounded(self, board):
        y, x = self.pos
        i = 0
        for s_y, s_x in [(y+1,x),(y-1,x),(y,x-1),(y,x+1)]:
                if {board[s_y][s_x]} == board.classes.difference({self.type}):
                    i += 1
        if i == 4:
            return True
        else:
            return False

    def next_space(self, board: 'Board'):
        if self.is_engaged(board):
            return self.pos
        elif self.is_surrounded(board):
            return self.pos
        else:
            target = self.target(board)
            move_score = {}
            free = get_empty_surround(self.pos, board)
            for space in free:
                move_score[space] = distance(space, target)
            move_score[self.pos] = distance(self.pos, target)

            top =  top_reading_order(move_score)
            print(self)
            print(target, move_score, free)
            print(top)
            return top

    def next_space2(self, board: 'Board') -> Tuple[int, int]:
        target_dist = copy.deepcopy(board)
        if self.is_engaged(target_dist):
            del target_dist
            return self.pos
        elif self.is_surrounded(target_dist):
            del target_dist
            return self.pos
        else:
            target = self.target(target_dist)
            if target != None:

                d = 0
                target_dist[target[0]][target[1]] = d

                next_s = []
                while len(next_s) == 0: 
                    for y, row in enumerate(target_dist):
                        for x, val in enumerate(row):
                            if val == d:
                                surround = get_empty_surround((y,x), target_dist)
                                for y,x in surround:
                                    target_dist[y][x] = d +1
                    digits = []
                    for y,x in get_surround(self.pos,target_dist):
                        if type(target_dist[y][x]) == int:
                            t = target_dist[y][x]
                            digits.append((y,x,t))
                    if len(digits) > 0:
                        digits.sort(key = lambda x: (x[2],x[0],x[1]))
                        next_s.append(digits[0][0:2])

                    # print(self.pos,target)
                    # print_target(target_dist)
                    d += 1
                del target_dist
                return next_s[0]

            del target_dist
            return self.pos

    def find_attack(self, board):
        potential = list()
        y,x = self.pos
        for s_y, s_x in [(y+1, x), (y-1, x), (y, x-1), (y, x+1)]:
            if {board[s_y][s_x]} == board.classes.difference({self.type}):
                potential.append((s_y,s_x))
        
        attack = []
        for char in board.characters:
            if char.pos in potential:
                attack.append((*char.pos,char.hp))

        attack.sort(key = lambda x: (x[2], x[0], x[1]))
        return attack[0]
    
    def find_enemies(self,board):
        enemies = [char for char in board.characters if char.type != self.type]

        if len(enemies) == 0:
            return False
        
        else:
            return True


                    

        
class Board(list):
    def __init__(self, board: str):
        super().__init__(self.make_board(board))
        self.characters = self.make_characters()
        self.classes = {'E','G'}
        self.turn = 0

    def make_board(self, board: str) -> List[str]:
        return [list(row) for row in board.split('\n')]

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self)
    
    def make_characters(self) -> List[Character]:
        characters = []
        for y, row in enumerate(self):
            for x, sym in enumerate(row):
                if sym in {'G', 'E'}:
                    characters.append(
                        Character(sym, (y,x))
                    )

        characters.sort(key = lambda x: (x.pos[0],x.pos[1]))
        return characters
    
    def all_empty(self) -> int:
        return len([i for row in self for i in row if i == '.'])

    def highlight(self, a, b = None):
        cp = copy.deepcopy(self)
        cp[a[0]][a[1]] = '()'
        if b:
            cp[b[0]][b[1]] = '[]'
        print(cp)
        del cp
    
    def check_path(self, a: Tuple [int,int], b: Tuple[int, int]) -> bool:
        initial_points = get_empty_surround(a, self)
        paths = set()
        for point in initial_points:
            paths.add(point)
        while True:
            old = paths.copy()
            for path in old:
                new = get_empty_surround(path, self)
                for point in new:
                    paths.add(point)
            if b in paths:
                return True
            if paths == old:
                return False
        return False
    
    def battle_on(self):
        chars = [char.type for char in self.characters]
        if self.classes == set(chars):
            return True
        else:
            return False
    
    def tick(self) -> None:
        self.characters.sort(key = lambda x: (x.pos[0],x.pos[1]))

        print(self.turn)
        print(self)
        print(self.characters)
        print(self.battle_on())

        for char in self.characters:

            if not char.find_enemies(self):
                print('no enemies')
                self.turn -= 1
                return None

            if not char.is_engaged(self):

                y, x = char.pos
                n_y, n_x = char.next_space2(self)

                # move me
                if (y, x) != (n_y, n_x):
                    char.pos = (n_y, n_x)
                    self[y][x] = '.'
                    self[n_y][n_x] = char.type

        for char in self.characters:  
            #fight!
            if char.is_engaged(self):

                if char.fight == None:
                    char.fight = char.find_attack(self)

                for enemy in self.characters:
                    if enemy.pos == char.fight[0:2]:
                        enemy.hp -= 3


        for i, char in enumerate(self.characters):
            y, x = char.pos
            if char.hp < 0:
                self.characters.pop(i)
                self[y][x] = '.'

        for char in self.characters:
            if char.fight:
                if self[char.fight[0]][char.fight[1]] == '.':
                    char.fight = None
        

        if self.battle_on():
            self.turn += 1


            
        
# BOARD = Board(ex1)
# assert len(BOARD) == 5
# elf = BOARD.characters[0]
# assert elf.next_space(BOARD) == (1,2)
 
# BOARD = Board(EX)
# for i in range(5):
#     BOARD.tick()
#     print(BOARD)

def rungame(board):
    while board.battle_on():
        board.tick()

    s = sum(char.hp for char in board.characters)
    b = board.turn
    print(f'turn: {b}')
    print(f'sum: {s}')
    print(f'total: {s * b}')
    total = s * b
    return total

ex2 ='''#######   
#.G...# 
#...EG# 
#.#.#G# 
#..G#E# 
#.....#   
#######'''
# 47, 590 ✓
# assert rungame(Board(ex2)) == 27730

ex3="""#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""
# 37, 982 (turn correct, score over by 9) 
# assert rungame(Board(ex3)) == 36334

ex4="""#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
# 46, 859 (turn correct, score over by 2)
# assert rungame(Board(ex4)) == 39514

ex5="""#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
# 35, 793 ✓
# assert rungame(Board(ex5)) == 27755

ex6="""#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
# 54,536 (turn off by 1, correct score)
# assert rungame(Board(ex6)) == 28944

ex7 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""
# 20, 937 (turn off by 1, score over by 3)
# assert rungame(Board(ex7)) == 18740


# part 1
with open('data/data-day15.txt') as f:
    board = Board(f.read())

rungame(board)