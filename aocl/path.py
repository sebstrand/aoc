import numpy as np

from collections import deque
from aocl import neighbors_2d, PriorityQueue


def dijkstra(cost, start_pos=(0,0), end_pos=None, dtype=np.uint32):
    """Path finding using Dijkstra's algorithm. Returns just the path as a deque if an end_pos is specified, otherwise
    returns a tuple of (distances, prev). Distances then is a grid that contains the distance to every node and prev is
    a dict that maps each node (position) to the node used to get there.

    >>> dijkstra({d: np.ones((3,3)) for d in 'nswe'}, (0,0))
    (array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4]], dtype=uint32), {(1, 0): (0, 0), (0, 1): (0, 0), (1, 1): (0, 1), (0, 2): (0, 1), (2, 0): (1, 0), (1, 2): (0, 2), (2, 1): (1, 1), (2, 2): (1, 2)})

    >>> cost = np.ones((3,3))
    >>> cost[(0, 1)], cost[(1, 1)], cost[(1, 2)] = 2, 3, 4
    >>> dijkstra({d: cost for d in 'nswe'}, end_pos=(2,2), dtype=np.uint8)
    deque([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
    """
    rows, cols = cost['n'].shape
    distances = np.zeros((rows, cols), dtype=dtype) + np.inf
    distances[start_pos] = 0
    prev = dict()

    q = PriorityQueue()
    q.add(0, start_pos)
    while len(q) > 0:
        pos = q.pop()
        if pos == end_pos:
            break

        for direction, (n_pos, n_dist) in neighbors_2d(distances, pos, named=True, valid_only=True).items():
            if n_dist < np.inf:
                continue # visited

            n_cost = cost[direction][n_pos]
            if n_cost == np.inf:
                continue

            distance_to_n = distances[pos] + n_cost
            if distance_to_n < distances[n_pos]:
                distances[n_pos] = distance_to_n
                prev[n_pos] = pos
                q.add(distance_to_n, n_pos)

    if end_pos:
        return path_from_prev(prev, start_pos, end_pos)
    else:
        return distances, prev


def path_from_prev(prev, start_pos, end_pos):
    """Recreates a path from start_pos to end_pos based on a dict mapping each node to a previous node. Useful for
    creating a path from the data returned by dijkstra.

    >>> path_from_prev({(1, 1): (1, 0), (1, 0): (0, 0)}, (0, 0), (1, 1))
    deque([(0, 0), (1, 0), (1, 1)])
    """
    pos = end_pos
    if not prev.get(pos) and pos != start_pos: return deque()
    path = deque()
    while pos:
        path.appendleft(pos)
        pos = prev.get(pos)
    return path
