from aocl import *


def solve(input_file, size, p1=True):
    lines = read_lines(input_file)

    incoming = list(tuple(ints(line)) for line in lines)
    mem_size, n_bytes = size

    start = (0, 0)
    end = (mem_size[0]-1, mem_size[1]-1)

    if p1:
        memory = {p: True for p in incoming[:n_bytes]}
        _, prev = dijkstra(memory, mem_size, start=start, end=end)

        path = set(path_from_prev(prev, start, end))
        return len(path) - 1
    else:
        memory = {}
        path = None
        for pos in incoming:
            memory[pos] = True
            # Find new path if position on old path got blocked
            if path is None or pos in path:
                dist, path = dijkstra(memory, mem_size, start=start, end=end)
                path = set(path_from_prev(path, start, end))
                # show(memory, mem_size, path)
                if end not in dist:
                    # No path found
                    return pos


def show(memory, size, path=None):
    print(term_effect(BoxDraw.BLOCK['light'] * (size[1] + 2), Terminal.YELLOW))
    for y in range(size[1]):
        print(term_effect(BoxDraw.BLOCK['light'], Terminal.YELLOW), end='')
        for x in range(size[0]):
            if path and (x, y) in path:
                s = term_effect('O', Terminal.B_CYAN)
            else:
                s = term_effect(BoxDraw.BLOCK['light'], Terminal.YELLOW) if memory.get((x, y)) else '.'
            print(s, end='')
        print(term_effect(BoxDraw.BLOCK['light'], Terminal.YELLOW))
    print(term_effect(BoxDraw.BLOCK['light'] * (size[1] + 2), Terminal.YELLOW))


def dijkstra(memory, mem_size, start=(0, 0), end=None):
    distances = {start: 0}
    prev = dict()

    q = PriorityQueue()
    q.add(0, start)
    while len(q) > 0:
        pos = q.pop()
        if pos == end:
            break

        for neighbor in neighbors(pos, mem_size):
            if memory.get(neighbor):
                continue  # blocked

            distance_to_n = distances[pos] + 1
            if distance_to_n < distances.get(neighbor, 2**64):
                distances[neighbor] = distance_to_n
                prev[neighbor] = pos
                q.add(distance_to_n, neighbor)

    return distances, prev


def neighbors(pos, mem_size):
    for direction in 'nswe':
        if direction == 'n' and pos[1] > 0: yield pos[0], pos[1] - 1
        if direction == 's' and pos[1] < mem_size[1] - 1: yield pos[0], pos[1] + 1
        if direction == 'w' and pos[0] > 0: yield pos[0] - 1, pos[1]
        if direction == 'e' and pos[0] < mem_size[0] - 1: yield pos[0] + 1, pos[1]


def main():
    _input_file = 'input'
    expected = {
        'input': (278, (43, 12)),
        'example': (22, (6, 1)),
    }[_input_file]
    size = {
        'input': ((71, 71), 1024),
        'example': ((7, 7), 12),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], size=size, p1=True)
    run(__file__, solve, _input_file, expected[1], size=size, p1=False)


if __name__ == '__main__':
    main()
