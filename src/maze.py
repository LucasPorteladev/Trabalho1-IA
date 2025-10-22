# src/maze.py
from typing import List, Tuple, Iterable, Optional

Grid = List[List[str]]
Pos = Tuple[int, int]

class Maze:
    
    def __init__(self, grid: Grid):
        self.grid = grid
        self.H = len(grid)
        self.W = len(grid[0]) if self.H > 0 else 0
        self.start = self._find('S')
        self.goal = self._find('G')

    def _find(self, ch: str) -> Pos:
        for r in range(self.H):
            for c in range(self.W):
                if self.grid[r][c] == ch:
                    return (r, c)
        raise ValueError(f"Caractere '{ch}' não encontrado no grid")

    def in_bounds(self, p: Pos) -> bool:
        r, c = p
        return 0 <= r < self.H and 0 <= c < self.W

    def passable(self, p: Pos) -> bool:
        r, c = p
        return self.grid[r][c] != '#'

    def actions(self, p: Pos) -> List[str]:
        acts = []
        r, c = p
        candidates = {
            'N': (r-1, c),
            'S': (r+1, c),
            'O': (r, c-1),
            'L': (r, c+1),
        }
        for a, q in candidates.items():
            if self.in_bounds(q) and self.passable(q):
                acts.append(a)
        return acts

    def result(self, p: Pos, a: str) -> Pos:
        r, c = p
        delta = {'N':(-1,0), 'S':(1,0), 'O':(0,-1), 'L':(0,1)}
        if a not in delta:
            raise ValueError("Ação inválida")
        dr, dc = delta[a]
        q = (r+dr, c+dc)
        if not (self.in_bounds(q) and self.passable(q)):
            raise ValueError("Ação inválida em p")
        return q

    def step_cost(self, p: Pos, a: str, q: Pos) -> float:
        return 1.0

    def goal_test(self, p: Pos) -> bool:
        return p == self.goal

    @staticmethod
    def from_file(path: str) -> "Maze":
        with open(path, 'r', encoding='utf-8') as f:
            lines = [list(line.rstrip('\n')) for line in f if line.strip() != ""]
        return Maze(lines)
