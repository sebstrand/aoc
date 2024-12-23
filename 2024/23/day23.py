from collections import defaultdict
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    pairs = [splits(line, sep=('-',)) for line in lines]

    connections = defaultdict(set)
    for c1, c2 in pairs:
        connections[c1].add(c2)
        connections[c2].add(c1)

    if p1:
        return len(find_k3_t_cliques(connections))
    else:
        cliques = find_cliques(connections)
        return cliques[max(cliques.keys())]


def find_k3_t_cliques(connections):
    k3_t_cliques = set()
    for c1, connected_c1 in connections.items():
        if not c1.startswith('t'): continue
        for c2 in connected_c1:
            connected_c2 = connections[c2]
            for c3 in connected_c2:
                connected_c3 = connections[c3]
                if c1 in connected_c3:
                    clique = tuple(sorted((c1, c2, c3)))
                    k3_t_cliques.add(clique)

    return k3_t_cliques


def find_cliques(connections):
    cliques = {}
    for c1, connected_c1 in connections.items():
        clique = [c1]
        added = True
        while added:
            added = False
            for cn in connections[clique[-1]]:
                if cn in clique: continue
                cn_connections = connections[cn]
                if all(c in cn_connections for c in clique):
                    clique.append(cn)
                    added = True
        cliques[len(clique)] = ','.join(sorted(clique))
    return cliques


def main():
    _input_file = 'input'
    expected = {
        'input': (1344, 'ab,al,cq,cr,da,db,dr,fw,ly,mn,od,py,uh'),
        'example': (7, 'co,de,ka,ta'),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
