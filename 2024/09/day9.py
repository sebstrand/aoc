import numpy as np
from collections import defaultdict
from aocl import *


FREE = -1


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    sizes = list(int(c) for c in lines[0])
    disk = np.zeros(sum(sizes), dtype=np.int16)
    disk[:] = FREE

    files = []
    free = []
    location = 0
    for i, size in enumerate(sizes):
        if i % 2 == 0:
            file_id = i // 2
            disk[location:location + size] = file_id
            files.append((file_id, location, size))
        else:
            free.append((location, size))
        location += size

    if p1:
        move_blocks(disk, files)
    else:
        move_files(disk, files, free)

    return sum(used_block * disk[used_block] for used_block in np.nonzero(disk != FREE)[0])


def move_blocks(disk, files):
    for file_id, location, size in reversed(files):
        free = list(np.nonzero(disk == FREE)[0][:size])
        if free[0] >= location:
            # Can only move file blocks towards start of disk
            continue
        elif free[-1] > location:
            # New list of blocks overlaps existing file location
            used = list(range(location, location + size + 1))
            usable = sorted(free + used)
        else:
            usable = free
        disk[location:location + size] = FREE
        disk[usable[:size]] = file_id


def move_files(disk, files, free_list):
    free = defaultdict(PriorityQueue)
    max_size = max(size for _, size in free_list)
    for location, size in free_list:
        free[size].add(location, location)

    for file_id, file_location, file_size in reversed(files):
        for free_size in range(file_size, max_size + 1):
            if free_size not in free or len(free[free_size]) == 0: continue

            free_location = free[free_size].pop()
            if free_location > file_location:
                # Can only move files towards start of disk
                continue
            elif free_size >= file_size:
                disk[file_location:file_location + file_size] = FREE
                disk[free_location:free_location + file_size] = file_id
                if free_size > file_size:
                    # Reinsert smaller block
                    new_location = free_location + file_size
                    new_size = free_size - file_size
                    free[new_size].add(new_location, new_location)
                break


def main():
    _input_file = 'input2'
    expected = {
        'input': (6310675819476, 6335972980679),
        'input2': (None, 97898222299196),
        'example': (1928, 2858),
    }[_input_file]

    # run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
