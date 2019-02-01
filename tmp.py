from typing import List, Dict, Tuple, Optional

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