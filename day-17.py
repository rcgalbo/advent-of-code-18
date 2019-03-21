from typing import Dict, Tuple
import re

ex = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

reg = '^(x|y)=(\d*), (x|y)=(\d*)..(\d*)'


def parse_input(in_str: str) -> Dict[Tuple[int, int], str]:
    clay = {}
    lines = in_str.split('\n')
    for line in lines:
        c1, di, c2, dj1, dj2 = (
            int(i) if i.isdigit() else i for i in re.findall(reg, line)[0]
        )
        if c1 == 'x':
            for y in range(dj1, dj2 + 1):
                clay[(y, di)] = '#'
        else:
            for x in range(dj1, dj2):
                clay[(di, x)] = '#'
    return clay


exc = parse_input(ex)


def draw_scan(scan: Dict[Tuple[int, int], str]) -> None:

    xmin, xmax = min(c[1] for c in scan.keys()), max(c[1] for c in scan.keys())
    ymin, ymax = min(c[0] for c in scan.keys()), max(c[0] for c in scan.keys())

    s = ''
    for y in range(ymin - 1, ymax + 2):
        s = s + '\n'
        for x in range(xmin - 1, xmax + 2):
            if (y, x) not in scan.keys():
                s = s + '.'
            else:
                s = s + scan[(y,x)]
    print(s)


def fill(
    scan: Dict[Tuple[int, int], str], source: Tuple[int, int]
) -> Dict[Tuple[int, int], str]:
    scan[source] = '+'
    while True:
        y, x = source
        y += 1
        if not (y+1, x) in scan.keys():
            scan[(y, x)] = '|'
        else:
            pass
            


