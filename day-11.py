from typing import List, Tuple

def get_digit(number: int, index: int) -> int:
    return number // 10**index %10

def make_grid(serial: int) -> List[int]:

    grid = [[0 for _ in range(300)] 
            for _ in range(300)]


    for X in range(300):
        for Y in range(300):
            rack_id = X+10
            power_level = rack_id * Y
            power_level += serial
            power_level *= rack_id
            power_level = get_digit(power_level, 2) 
            power_level -= 5

            grid[Y][X] = power_level

    return grid

assert make_grid(8)[5][3] == 4
assert make_grid(71)[153][101] == 4
assert make_grid(39)[196][217] == 0
assert make_grid(57)[79][122] == -5


def sum_nXn(grid: List[int], dim: Tuple[int,int] = (3,3)) -> List[int]:

    sum_grid = [[0 for _ in range(300-dim[0])]
                    for Y in range(300-dim[1])]

    for X in range(300-dim[0]):
        for Y in range(300-dim[1]):

            sub = [x[X:X+dim[0]] for x in grid[Y:Y+dim[1]]]
            sum_grid[Y][X] = sum(sum(l) for l in sub)

    return sum_grid

tst_grid = make_grid(42)
tst_sum = sum_nXn(tst_grid,(3,3))
assert tst_sum[61][21] == 30

def get_max_coord(grid: List[int]) -> Tuple[int, int]:
    coords = (0,0)
    max_val = 0

    for X in range(len(grid)):
        for Y in range(len(grid)):

            if grid[Y][X] > max_val:
                max_val = grid[Y][X]
                coords = (X,Y)

    return coords
    
assert get_max_coord(tst_sum) == (21,61)

# find largest power
grid = make_grid(7857)
sum_grid = sum_nXn(grid, (3,3))
print(get_max_coord(sum_grid))

# part 2: get max sub grid for all ixi: from 1x1:300x300
levels = []
for i in range(1,300):
    sub = sum_nXn(grid, (i,i))
    coord = get_max_coord(sub)
    value = sub[coord[1]][coord[0]]
    levels.append((i, coord, value))
    
sorted(levels, key=lambda x: x[2], reverse=True)[0:2]