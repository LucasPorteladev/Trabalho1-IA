# src/search.py
from typing import Tuple, List, Dict, Optional, Callable
from collections import deque
import heapq
import time

Pos = Tuple[int,int]

class SearchResult:
    def __init__(self, found: bool, path: List[Pos], cost: float,
                 time: float, metrics: Dict):
        self.found = found
        self.path = path
        self.cost = cost
        self.time = time
        self.metrics = metrics

class Node:
    def __init__(self, state: Pos, parent: Optional['Node']=None, action: Optional[str]=None, g: float=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def path(self) -> List[Pos]:
        node, rev = self, []
        while node is not None:
            rev.append(node.state)
            node = node.parent
        return list(reversed(rev))

def _common_metrics_init():
    return {
        'nodes_generated': 0,
        'nodes_expanded': 0,
        'max_frontier_size': 0,
        'max_explored_size': 0
    }

def bfs_search(maze) -> SearchResult:
    start_time = time.perf_counter()
    metrics = _common_metrics_init()

    start = Node(maze.start, g=0.0)
    if maze.goal_test(start.state):
        return SearchResult(True, [start.state], 0.0, 0.0, metrics)

    frontier = deque([start])
    explored = set()
    metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(frontier))

    while frontier:
        node = frontier.popleft()
        metrics['nodes_expanded'] += 1
        explored.add(node.state)

        if maze.goal_test(node.state):
            elapsed = time.perf_counter() - start_time
            return SearchResult(True, node.path(), node.g, elapsed, metrics)

        for a in maze.actions(node.state):
            q = maze.result(node.state, a)
            metrics['nodes_generated'] += 1
            if q not in explored and not any(n.state == q for n in frontier):
                child = Node(q, parent=node, action=a, g=node.g + maze.step_cost(node.state, a, q))
                frontier.append(child)
                metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(frontier))
        metrics['max_explored_size'] = max(metrics['max_explored_size'], len(explored))

    elapsed = time.perf_counter() - start_time
    return SearchResult(False, [], float('inf'), elapsed, metrics)

def dfs_search(maze, depth_limit=None) -> SearchResult:
    start_time = time.perf_counter()
    metrics = _common_metrics_init()
    start = Node(maze.start, g=0.0)
    if maze.goal_test(start.state):
        return SearchResult(True, [start.state], 0.0, 0.0, metrics)

    frontier = [start]  # stack
    explored = set()
    metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(frontier))

    while frontier:
        node = frontier.pop()
        metrics['nodes_expanded'] += 1
        explored.add(node.state)

        if maze.goal_test(node.state):
            elapsed = time.perf_counter() - start_time
            return SearchResult(True, node.path(), node.g, elapsed, metrics)

        # optional depth limit
        if depth_limit is None or node.g < depth_limit:
            for a in maze.actions(node.state):
                q = maze.result(node.state, a)
                metrics['nodes_generated'] += 1
                if q not in explored and not any(n.state == q for n in frontier):
                    child = Node(q, parent=node, action=a, g=node.g + maze.step_cost(node.state, a, q))
                    frontier.append(child)
                    metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(frontier))
        metrics['max_explored_size'] = max(metrics['max_explored_size'], len(explored))

    elapsed = time.perf_counter() - start_time
    return SearchResult(False, [], float('inf'), elapsed, metrics)

def _push_heap(heap, priority, counter, node):
    heapq.heappush(heap, (priority, counter, node))

def greedy_search(maze, heuristic: Callable[[Pos, Pos], float]) -> SearchResult:
    start_time = time.perf_counter()
    metrics = _common_metrics_init()
    start = Node(maze.start, g=0.0)
    if maze.goal_test(start.state):
        return SearchResult(True, [start.state], 0.0, 0.0, metrics)

    heap = []
    counter = 0
    _push_heap(heap, heuristic(start.state, maze.goal), counter, start)
    metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(heap))
    explored = set()

    while heap:
        _, _, node = heapq.heappop(heap)
        metrics['nodes_expanded'] += 1
        if node.state in explored:
            continue
        explored.add(node.state)

        if maze.goal_test(node.state):
            elapsed = time.perf_counter() - start_time
            return SearchResult(True, node.path(), node.g, elapsed, metrics)

        for a in maze.actions(node.state):
            q = maze.result(node.state, a)
            metrics['nodes_generated'] += 1
            if q not in explored:
                child = Node(q, parent=node, action=a, g=node.g + maze.step_cost(node.state, a, q))
                counter += 1
                priority = heuristic(child.state, maze.goal)
                _push_heap(heap, priority, counter, child)
                metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(heap))
        metrics['max_explored_size'] = max(metrics['max_explored_size'], len(explored))

    elapsed = time.perf_counter() - start_time
    return SearchResult(False, [], float('inf'), elapsed, metrics)

def a_star_search(maze, heuristic: Callable[[Pos, Pos], float]) -> SearchResult:
    start_time = time.perf_counter()
    metrics = _common_metrics_init()
    start = Node(maze.start, g=0.0)
    if maze.goal_test(start.state):
        return SearchResult(True, [start.state], 0.0, 0.0, metrics)

    open_heap = []
    counter = 0
    start_f = start.g + heuristic(start.state, maze.goal)
    _push_heap(open_heap, start_f, counter, start)

    came_from = {start.state: start}
    g_score = {start.state: 0.0}
    closed = set()
    metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(open_heap))

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current.state in closed:
            continue

        metrics['nodes_expanded'] += 1
        if maze.goal_test(current.state):
            elapsed = time.perf_counter() - start_time
            return SearchResult(True, current.path(), current.g, elapsed, metrics)

        closed.add(current.state)

        for a in maze.actions(current.state):
            q = maze.result(current.state, a)
            tentative_g = current.g + maze.step_cost(current.state, a, q)
            metrics['nodes_generated'] += 1

            if q in closed:
                continue

            if q not in g_score or tentative_g < g_score[q]:
                child = Node(q, parent=current, action=a, g=tentative_g)
                g_score[q] = tentative_g
                counter += 1
                f = tentative_g + heuristic(q, maze.goal)
                _push_heap(open_heap, f, counter, child)
                metrics['max_frontier_size'] = max(metrics['max_frontier_size'], len(open_heap))

        metrics['max_explored_size'] = max(metrics['max_explored_size'], len(closed))

    elapsed = time.perf_counter() - start_time
    return SearchResult(False, [], float('inf'), elapsed, metrics)
