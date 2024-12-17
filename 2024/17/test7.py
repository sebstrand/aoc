
program = [2, 4, 1, 2, 7, 5, 4, 5, 0, 3, 1, 7, 5, 5, 3, 0]

#for a in range(0, 8**len(program)):
best = 0
for a in range(187025214891616 - 1, 211106165767183 + 1, 8):
    i = 0
    start_a = a
    while a > 0:
        calc_o = ((((a % 8) ^ 2) ^ (a // 2 ** ((a % 8) ^ 2))) ^ 7) % 8
        if calc_o != program[i]:
            break
        a //= 8
        i += 1
    if i == len(program):
        print('FOUND IT!  A ==', start_a)
        break
    elif i > best:
        best = i
        print('best', best, start_a)


