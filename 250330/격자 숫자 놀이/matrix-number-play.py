'''
시간복잡도
100*100*100

2차원 배열의 값은 100이 최대임
'''
from collections import Counter

er, ec, num = map(int, input().split())
er -= 1
ec -= 1
grid = [list(map(int, input().split())) for i in range(3)]
ans = -1


def sort():
    global grid
    new_grid = []
    max_len = 0
    for row in grid:
        cnt = Counter(row)
        tmp = []
        for k, v in cnt.items():
            if k != 0:
                tmp.append([k, v])
        tmp.sort(key=lambda x: (x[1], x[0]))
        new_row = []
        for _ in tmp:
            new_row.extend(_)
        max_len = max(max_len, len(new_row))
        new_grid.append(new_row)
    for _ in new_grid:
        if len(_) < max_len:
            _.extend([0] * (max_len - len(_)))
    grid = new_grid


for t in range(1, 101):  # 100초까지 가능
    if len(grid) >= len(grid[0]):
        sort()

    else:
        grid = list(zip(*grid))
        sort()
        grid = list(zip(*grid))


    grid = [_[:100] for _ in grid[:100]]
    if len(grid) > er and len(grid[0]) > ec and grid[er][ec] == num:
        ans = t
        break

print(ans)