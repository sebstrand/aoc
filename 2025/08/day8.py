from aocl import *
import math


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    junctions = []
    for line in lines:
        x, y, z = ints(line)
        junctions.append(p3d(y, x, z))

    if p1:
        # 10 in example, 1000 in real input
        wanted_connections = 10 if len(junctions) < 100 else 1000
    else:
        wanted_connections = len(junctions)**2

    # create map from squared distance to junction pair
    dist_to_junctions = {}
    for i, j1 in enumerate(junctions):
        for j2 in junctions[i+1:]:
            dist_to_junctions[dist_sq(j1, j2)] = (j1, j2)

    # start with 1 circuit per junction
    circuits = {j: i for i, j in enumerate(junctions)}
    counts = {c: 1 for c in circuits.values()}

    max_circuit_size = 1
    sorted_distances = sorted(dist_to_junctions.keys())
    for wanted_dist in sorted_distances[:wanted_connections]:
        j1, j2 = dist_to_junctions[wanted_dist]
        c1 = circuits[j1]
        c2 = circuits[j2]
        if c1 == c2: continue  # already connected

        for junction, circuit in circuits.items():
            if circuit == c2:
                circuits[junction] = c1
        counts[c1] += counts[c2]
        counts[c2] = 0
        max_circuit_size = max(max_circuit_size, counts[c1])
        if not p1 and max_circuit_size == len(junctions):
            return j1.x * j2.x

    return math.prod(list(sorted(counts.values(), reverse=True))[:3])


def dist_sq(p1, p2):
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2


def main():
    _input_file = 'input'
    expected = {
        'input': (103488, 8759985540),
        'example': (40, 25272),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
