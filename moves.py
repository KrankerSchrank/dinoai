moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2],
}

i = 0
for j in range(3):
    for k in range(3):
        for l in range(1,10):
            print(f'{i}: [{j}, {k}, {moves[l][0]}, {moves[l][1]}],')
            i=i+1
