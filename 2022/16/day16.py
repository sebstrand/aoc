import numpy as np
from aocl import *


remaining_time = 30


def solve(input_file, num_agents=1):
    lines = read_lines(input_file)

    valves = []
    for i, line in enumerate(lines):
        parts = splits(line.replace(';', ''))
        valve = parts[1]
        flow = int(parts[4][5:])
        leads_to = list(v[:2] for v in parts[9:])
        valves.append({
            'name': valve,
            'flow': flow,
            'leads_to': leads_to,
            'open': False
        })

    start_valve = 'AA'
    adjacent, valves = create_optimized_adjacency_matrix(valves, start_valve=start_valve)
    start_index = None
    for i, valve in enumerate(valves):
        valve['idx'] = i
        if valve['name'] == start_valve:
            start_index = i

    distances = calc_distances(adjacent)

    max_time = remaining_time - (num_agents - 1) * 4
    agents = list((0, start_index, 'A' + str(n)) for n in range(num_agents))
    valves = list(v for v in valves if v['flow'] > 0)
    return calc_max_flow(valves, distances, agents, max_time=max_time)


def calc_max_flow(valves, distances, agents, max_time, taken_valves=None, level=0):
    if taken_valves is None:
        taken_valves = set()

    best_flow = 0
    time_now, agent_location, agent_name = agents[0]

    for valve in valves:
        valve_location = valve['idx']
        if valve_location in taken_valves:
            continue
        dist_to_valve = distances[agent_location][valve_location]
        flow_time = max_time - time_now - dist_to_valve - 1
        if flow_time > 0:
            valve_flow = flow_time * valve['flow']

            new_agents = agents[1:]
            new_agents.append((time_now + dist_to_valve + 1, valve_location, agent_name))
            new_agents.sort(key=lambda agent: agent[0])

            remaining_best_flow = calc_max_flow(
                valves,
                distances,
                new_agents,
                max_time=max_time,
                taken_valves=taken_valves | {valve['idx']},
                level=level + 2,
            )

            if valve_flow + remaining_best_flow > best_flow:
                best_flow = valve_flow + remaining_best_flow

    return best_flow


def calc_distances(adjacent):
    num_valves = len(adjacent)
    distances = np.zeros((num_valves, num_valves))
    for i in range(num_valves):
        for j in range(i + 1, num_valves):
            dist, prev = dijkstra(adjacent, start_vertex=i, end_vertex=j)
            distances[i, j] = dist[j]
            distances[j, i] = dist[j]
    return distances


def create_optimized_adjacency_matrix(valves, start_valve):
    valve_index = {valve['name']: i for i, valve in enumerate(valves)}

    # Create initial adjacency matrix
    adjacent = np.zeros((len(valves), len(valves)), dtype=np.uint8)
    for i, valve in enumerate(valves):
        for other in valve['leads_to']:
            j = valve_index[other]
            adjacent[i][j] = 1

    # Remove valves with no flow (except AA) from graph
    for i, valve in enumerate(valves):
        if valve['name'] != start_valve and valve['flow'] == 0:  # no flow
            # Connect all our neighbors to all other neighbors
            for n1 in np.nonzero(adjacent[i])[0]:
                for n2 in np.nonzero(adjacent[i])[0]:
                    if n1 != n2:
                        # Make a direct connection from n1 to n2 with distance set to the distance
                        # from us to each of them. If they were already connected, make sure to not
                        # increase distance
                        dist = adjacent[i][n1] + adjacent[i][n2]
                        if adjacent[n1][n2] > 0:
                            dist = min(dist, adjacent[n1][n2])
                        adjacent[n1][n2] = dist
                        adjacent[n2][n1] = dist
            # Remove this node from graph
            adjacent[i, :] = 0
            adjacent[:, i] = 0

    adjacent_small = adjacent
    for i, row in enumerate(reversed(adjacent)):
        idx = len(adjacent) - i - 1
        if not row.any() and not row[idx]:
            adjacent_small = np.delete(adjacent_small, idx, axis=0)
            adjacent_small = np.delete(adjacent_small, idx, axis=1)
            del valves[idx]

    return adjacent_small, valves


def main():
    _input_file = 'input'
    expected = {
        'input': (2080, 2752),
        'example': (1651, 1707),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], num_agents=1)
    run(__file__, solve, _input_file, expected[1], num_agents=2)


if __name__ == '__main__':
    main()
