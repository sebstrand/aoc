import numpy as np
from aocl import *
from collections import defaultdict


def solve(input_file):
    lines = read_lines(input_file)

    components = defaultdict(set)
    for line in lines:
        lbl = labeline(line, numbered=False)
        components[lbl.label].update(splits(lbl.content))
        for connection in components[lbl.label]:
            components[connection].add(lbl.label)

    a, b = spectral_partition(components)

    bridges = 0
    for c in a:
        bridges += sum(connection not in a for connection in components[c])
    print('Bridges:', bridges)
    assert bridges == 3

    print('|a|, |b|', len(a), len(b))
    return len(a) * len(b)


def spectral_partition(components):
    component_names = list(components.keys())
    n = len(component_names)

    # Create symmetric adjacency matrix (1 for each connected component pair)
    adjacency = np.zeros((n, n), dtype=np.float32)
    for i, connections in enumerate(components.values()):
        for connection in connections:
            j = component_names.index(connection)
            adjacency[i, j] = 1

    # Create degree matrix (number of component connections on diagonal)
    degree = np.zeros((n, n), dtype=np.float32)
    for i, connections in enumerate(components.values()):
        degree[i, i] = len(connections)

    # Get Fiedler vector (2nd Eigenvector) from Laplacian matrix
    laplace = degree - adjacency
    _, eig_vec = np.linalg.eigh(laplace)
    eig_vec2 = eig_vec[:, 1]

    # Partition using sign of Fiedler vector
    a = set(c for i, c in enumerate(component_names) if eig_vec2[i] >= 0)
    b = set(c for i, c in enumerate(component_names) if eig_vec2[i] < 0)
    return a, b


def main():
    _input_file = 'input'
    expected = {
        'input': 600369,
        'example': 54,
    }[_input_file]

    run(__file__, solve, _input_file, expected)


if __name__ == '__main__':
    main()
