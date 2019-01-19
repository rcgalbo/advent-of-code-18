from typing import Dict

with open('data/data-day12.txt') as f:
    initial_state = '...' + f.readline().strip().replace('initial state: ','')
    _ = f.readline()
    raw = [l.strip().split(' => ') for l in f.readlines()]
    rules = {l[0]: l[1] for l in raw}
    

def test_generation(past_state: str, rules: Dict[str,str]) -> str:
    state = [p for p in past_state]
    for i in range(3,len(past_state)-3):
        pattern=past_state[i-2:i+3]
        if pattern in rules.keys():
            update = rules[pattern]
        else:
            update = '.'
        state[i] = update
        
    return ''.join(state)
    
def generation(past_state: str, rules: Dict[str,str]) -> str:
    state = list(past_state) + list('.'*3)
    for i in range(2,len(past_state)):
        start = i -2
        stop = i + 3
        if stop > len(past_state):
            new_pots = stop - len(past_state)
            past_state = past_state + '.'*new_pots
        pattern = past_state[start:stop]
        update = rules[pattern]
        state[i] = update
        
    return ''.join(state)

test_initial = '...' + '#..#.#..##......###...###...........'
test_rule_input = '''...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''
test_rules_raw = [l.split(' => ') for l in test_rule_input.split('\n')]
test_rules = {l[0]: l[1] for l in test_rules_raw}

assert test_generation(test_initial, test_rules) == '...#...#....#.....#..#..#..#...........'

# count plants starting at -3
test_end = '.#....##....#####...#######....#.#..##.'
count_plants = lambda x: sum(i for i,j in enumerate(x,start=-3) if j == '#')
assert count_plants(test_end) == 325


# part 1 
print("0    :",initial_state)
geni = generation(initial_state,rules)
print("1    :", geni)
for i in range(2,21):
    geni = generation(geni, rules)
    print(i,'   :',geni)

print(count_plants(geni))


# part 2
print("0    :",initial_state)
geni = generation(initial_state,rules)
print("1    :", geni)
for i in range(2,115):
    last = count_plants(geni)
    geni = generation(geni, rules)
    print(i, 'now', count_plants(geni), 'diff', count_plants(geni) - last)

# converges to 23 after 111
ifirst111 = count_plants(geni)
rest = (50000000000 - 111) * 23