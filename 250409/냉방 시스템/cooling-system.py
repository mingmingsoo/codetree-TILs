from collections import deque

n, bn, limit = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
block = [[[0] * 4 for i in range(n)] for i in range(n)]
for b in range(bn):
    r, c, s = map(int, input().split())
    r -= 1
    c -= 1
    if s == 0:
        block[r][c][1] = 1
        block[r - 1][c][3] = 1
    else:
        block[r][c][0] = 1
        block[r][c - 1][2] = 1

aircon = set()
valid = set()
for i in range(n):
    for j in range(n):
        if 2 <= grid[i][j] <= 5:
            aircon.add((i, j, grid[i][j] - 2))
            grid[i][j] = 0
        elif grid[i][j] == 1:
            valid.add((i, j))
            grid[i][j] = 0

# 미리 채워지는 맵 만들어놓기
fill = [[0] * n for i in range(n)]
dir_dict = {0: (1, 3), 1: (0, 2), 2: (1, 3), 3: (0, 2)}
row = [0, -1, 0, 1]
col = [-1, 0, 1, 0]
for r, c, s in aircon:
    tmp = [[0] * n for i in range(n)]
    # 바로 밑은 5로 무조건
    nr = r + row[s]
    nc = c + col[s]
    tmp[nr][nc] = 5
    q = deque([(nr, nc, 4)])
    while q:
        r, c, power = q.popleft()
        if power == 0:
            break
        # 바로 그 방향
        nr = r + row[s]
        nc = c + col[s]
        if 0 <= nr < n and 0 <= nc < n and not block[r][c][s] and not tmp[nr][nc]:
            q.append((nr, nc, power - 1))
            tmp[nr][nc] = power

        for d in dir_dict[s]:
            nr1 = r + row[d]
            nc1 = c + col[d]

            nr2 = nr1 + row[s]
            nc2 = nc1 + col[s]

            if 0 <= nr1 < n and 0 <= nc1 < n and 0 <= nr2 < n and 0 <= nc2 < n and not block[r][c][d] and not \
                    block[nr1][nc1][s] and not tmp[nr2][nc2]:
                tmp[nr2][nc2] = power
                q.append((nr2, nc2, power - 1))
    for i in range(n):
        for j in range(n):
            fill[i][j] += tmp[i][j]
ans = -1


def end():
    for vr, vc in valid:
        if grid[vr][vc] < limit:
            return False
    return True


for t in range(101):

    # 0. 검증쓰
    if end():
        ans = t
        break

    # 1. 온풍쓰
    for i in range(n):
        for j in range(n):
            grid[i][j] += fill[i][j]

    # 2. 시원한 공기 섞이기
    plus = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] < grid[i][j]:
                    diff = (grid[i][j] - grid[nr][nc]) // 4
                    if not block[i][j][k]:
                        plus[nr][nc] += diff
                        plus[i][j] -= diff

    for i in range(n):
        for j in range(n):
            grid[i][j] += plus[i][j]

    # 가생이 빼줘잉
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                if grid[i][j]:
                    grid[i][j] -= 1
print(ans)
