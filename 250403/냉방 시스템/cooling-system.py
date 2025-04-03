'''
역시 어렵군
'''
from collections import deque

row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]

n, b, limit = map(int, input().split())
aircon = set()
grid = [list(map(int, input().split())) for i in range(n)]
valid_set = set()
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            valid_set.add((i, j))
            grid[i][j] = 0
        elif 2 <= grid[i][j] <= 5:
            aircon.add((grid[i][j], i, j))
            grid[i][j] = 0

block = [[[False] * 4 for i in range(n)] for i in range(n)]
for _ in range(b):
    r, c, s = map(int, input().split())
    r -= 1
    c -= 1
    if s == 0:
        block[r][c][0] = True
        block[r - 1][c][2] = True
    if s == 1:
        block[r][c][3] = True
        block[r][c - 1][1] = True

real_fill = [[0] * n for i in range(n)]
edge_set = set()
for i in range(n):
    for j in range(n):
        if i == 0 or i == n - 1 or j == 0 or j == n - 1:
            edge_set.add((i, j))
dir_dict = {2: 6, 3: 0, 4: 2, 5: 4}

side_dict = {2: (0, 4, 6), 3: (6, 2, 0), 4: (0, 4, 2), 5: (6, 2, 4)}
for shape, sr, sc in aircon:
    fill = [[0] * n for i in range(n)]
    fill[sr + row[dir_dict[shape]]][sc + col[dir_dict[shape]]] = 5
    q = deque([(sr + row[dir_dict[shape]], sc + col[dir_dict[shape]], 5)])
    # 5는 무조건 시원해져
    while q:
        r, c, power = q.popleft()
        if power == 1:
            break
        # 바로 밑에
        k = dir_dict[shape]
        nr = r + row[k]
        nc = c + col[k]
        if 0 <= nr < n and 0 <= nc < n and not block[r][c][k // 2]:
            fill[nr][nc] = power - 1
            q.append((nr, nc, power - 1))

        # 옆에
        for k in side_dict[shape][:2]:
            nr1 = r + row[k]
            nc1 = c + col[k]

            nr2 = nr1 + row[side_dict[shape][2]]
            nc2 = nc1 + col[side_dict[shape][2]]
            if not (0 <= nr1 < n and 0 <= nc1 < n) or block[r][c][k // 2]:
                continue
            if not (0 <= nr2 < n and 0 <= nc2 < n) or block[nr1][nc1][side_dict[shape][2] // 2]:
                continue
            fill[nr2][nc2] = power - 1
            q.append((nr2, nc2, power - 1))


    for i in range(n):
        for j in range(n):
            if fill[i][j]:
                real_fill[i][j] += fill[i][j]

ans = -1


def valid():
    for vr, vc in valid_set:
        if grid[vr][vc] < limit:
            return False
    return True


def edge():
    for er, ec in edge_set:
        if grid[er][ec]:
            grid[er][ec] -= 1


def filling():
    for i in range(n):
        for j in range(n):
            if real_fill[i][j]:
                grid[i][j] += real_fill[i][j]


def spread():
    plus_grid = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                continue
            for k in (0, 2, 4, 6):
                nr = i + row[k]
                nc = j + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or block[i][j][k // 2] or grid[nr][nc] >= grid[i][j]:
                    continue
                diff = (grid[i][j] - grid[nr][nc]) // 4
                plus_grid[nr][nc] += diff
                plus_grid[i][j] -= diff

    for i in range(n):
        for j in range(n):
            grid[i][j] += plus_grid[i][j]


for t in range(1, 101):
    filling()
    spread()
    edge()
    if valid():
        ans = t
        break

print(ans)