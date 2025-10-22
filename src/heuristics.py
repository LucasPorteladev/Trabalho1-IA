# src/heuristics.py
from typing import Tuple
Pos = Tuple[int,int]
import math

def h_manhattan(a: Pos, b: Pos) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def h_euclidean(a: Pos, b: Pos) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])
