# day 9: marble mania
from typing import NamedTuple, List
from collections import defaultdict

# winning score:
# parameters last score, number players

# gameplay 

# player insert marble between 1 and 2 marbles clockwise of current
# marble % 23 == 0 player keeps marble, removes marble 7 counter-clockwise
# marble clockwise becomes new current marble

class Circle(list):
    def __init__(self, *args):
        list.__init__(self,*args)
        self.append(0)
        self.append(1)


    def clockwise_insert(self, index, value, offset = 2):
        if index + offset > len(self):
            index = (index + offset) % len(self)
            self.insert(index, value)
        else:
            index = index + offset
            self.insert(index,value)
        return index


    def get_counter_clockwise(self,index,offset=7):
        i = index - offset
        if i < 0:
            i = len(self) + i
        return i, self.pop(i)


class Game(NamedTuple):
    players: int
    last_marble: int
    board: 'Circle'


def play(game: 'Game') -> int:
    current = 2
    last_index = 1
    last_score = 0
    scores = defaultdict(int)

    while current <= game.last_marble:

        #score increase
        if current % 23 == 0:

            player = current % game.players
            last_index, removed = game.board.get_counter_clockwise(last_index)

            score = current + removed

            scores[player] += score 

            current += 1

        last_index = game.board.clockwise_insert(last_index,current)
        current += 1

    return sorted(scores.values(), reverse=True)[0]


# assert play(Game(9,25,Circle())) == 32
# assert play(Game(10,1618,Circle())) == 8317
# assert play(Game(17,1104,Circle())) == 2764
# assert play(Game(21,6111,Circle())) == 54718
# assert play(Game(30,5807,Circle())) == 37305
# assert play(Game(13,7999,Circle())) == 146373


in_str = "468 players; last marble is worth 71010 points"
print(play(Game(468,71010, Circle())))

#part2
print(play(Game(468,71010*100, Circle())))