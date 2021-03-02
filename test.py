for i in range(24, 88, 2):
    print(f'let map1_x[{i}] = 15;')
    print(f'let map1_y[{i}] = {int(i/2-12)};')
    print(f'let map1_x[{i+1}] = 0;')
    print(f'let map1_y[{i+1}] = {int(i/2-12)};')
print('-------------------------')
for i in range(24, 88, 2):
    print(f'let map_x[{i}] = {16*int(i/2-12)};')
    print(f'let map_y[{i}] = 240;')
    print(f'let map_x[{i+1}] = {16*int(i/2-12)};')
    print(f'let map_y[{i+1}] = 0;')