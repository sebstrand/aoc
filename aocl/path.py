import numpy as np

from collections import deque
from aocl import neighbors_2d, PriorityQueue


def dijkstra_grid(cost, start_pos=(0, 0), end_pos=None):
    """Path finding in a grid using Dijkstra's algorithm. Cost should be a dict of 2d numpy arrays signifying he cost of
    moving to that position when going in the direction that is the dict key (nswe). Costs that are negative or np.inf
    will be considered invalid moves. Returns a tuple of (distances, prev). Distances is a grid that contains the
    distance to every node and prev is a dict that maps each node (position) to the node used to get there. Specify
    end_pos to stop when distance to that position has been found, in that case the distances grid will be incomplete.

    >>> dist, prev = dijkstra_grid({d: np.ones((3,3)) for d in 'nswe'}, (0,0))
    >>> dist
    array([[0., 1., 2.],
           [1., 2., 3.],
           [2., 3., 4.]])
    >>> str(prev).replace(' ', '')
    '{(1,0):(0,0),(0,1):(0,0),(1,1):(0,1),(0,2):(0,1),(2,0):(1,0),(1,2):(0,2),(2,1):(1,1),(2,2):(1,2)}'
    """
    rows, cols = cost['n'].shape
    distances = np.zeros((rows, cols)) + np.inf
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
                continue  # visited

            n_cost = cost[direction][n_pos]
            if n_cost < 0 or n_cost == np.inf:
                continue

            distance_to_n = distances[pos] + n_cost
            if distance_to_n < distances[n_pos]:
                distances[n_pos] = distance_to_n
                prev[n_pos] = pos
                q.add(distance_to_n, n_pos)

    return distances, prev


def dijkstra(edges, start_vertex=0, end_vertex=None):
    """Path finding using Dijkstra's algorithm with an adjacency matrix as input. Each row in the adjacency matrix
    should map the distance from vertex <row> to vertex <col>. A zero means there is no edge (in that direction) between
    the vertices. Returns just the path as a deque if an end_pos is specified, otherwise returns a tuple of
    (distances, prev). Distances then is a grid that contains the distance to every node and prev is a dict that maps
    each node (position) to the node used to get there. Specify end_vertex to stop when distance to that vertex has been
    found.

    >>> e = np.array([[0, 1, 0, 0],[0, 0, 2, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
    >>> dijkstra(e, 0)
    (array([0., 1., 3., 4.]), {1: 0, 2: 1, 3: 2})
    """
    n_vertices = edges.shape[0]
    distances = np.zeros(n_vertices) + np.inf
    distances[start_vertex] = 0
    prev = dict()

    q = PriorityQueue()
    q.add(0, start_vertex)
    while len(q) > 0:
        vertex = q.pop()
        if vertex == end_vertex:
            break

        row = edges[vertex]
        for v_neighbor in np.nonzero(row)[0]:
            if distances[v_neighbor] < np.inf:
                continue  # visited

            edge_dist = row[v_neighbor]
            distance_to_n = distances[vertex] + edge_dist
            if distance_to_n < distances[v_neighbor]:
                distances[v_neighbor] = distance_to_n
                v_neighbor = int(v_neighbor)
                prev[v_neighbor] = vertex
                q.add(float(distance_to_n), v_neighbor)

    return distances, prev


def path_from_prev(prev, start_pos, end_pos):
    """Recreates a path from start_pos to end_pos based on a dict mapping each node to a previous node. Useful for
    creating a path from the data returned by dijkstra.

    >>> path_from_prev({(1, 1): (1, 0), (1, 0): (0, 0)}, (0, 0), (1, 1))
    deque([(0, 0), (1, 0), (1, 1)])
    """
    pos = end_pos
    if pos not in prev and pos != start_pos: return deque()
    path = deque()
    while pos is not None:
        path.appendleft(pos)
        pos = prev.get(pos)
    return path


def manhattan(pos1, pos2):
    if pos1 == pos2:
        return 0
    return abs(pos1.y - pos2.y) + abs(pos1.x - pos2.x)
