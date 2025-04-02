'''
백준하고 문제 다름;;;;
'''
from collections import deque

poww, _ = map(int, input().split())
n = 2 ** (poww)

grid = [list(map(int, input().split())) for i in range(n)]
level_lst = list(map(int, input().split()))


def rotation(si, sj, level, half):  # half칸 씩 회전..?
    small_grid = [_[sj:sj + level] for _ in grid[si:si + level]]

    small_grid1 = [_[:half] for _ in small_grid[:half]]
    small_grid2 = [_[half:level] for _ in small_grid[:half]]
    small_grid3 = [_[:half] for _ in small_grid[half:level]]
    small_grid4 = [_[half:level] for _ in small_grid[half:level]]

    # 이걸 회전
    small_grid_lo = [[0] * level for i in range(level)]
    for i in range(half):
        for j in range(half):
            small_grid_lo[i][j] = small_grid3[i][j]
    for i in range(half):
        for j in range(half, level, 1):
            small_grid_lo[i][j] = small_grid1[i][j - half]

    for i in range(half, level, 1):
        for j in range(half):
            small_grid_lo[i][j] = small_grid4[i - half][j]

    for i in range(half, level, 1):
        for j in range(half, level, 1):
            small_grid_lo[i][j] = small_grid2[i - half][j - half]

    for i in range(level):
        for j in range(level):
            grid[i+si][j+sj] = small_grid_lo[i][j]


row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
for l in level_lst:
    level = 2 ** l

    for i in range(0, n, level):
        for j in range(0, n, level):
            rotation(i, j, level, level // 2)

    melting = [[0] * n for i in range(n)]
    # 얼음 녹이기
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                cnt = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
                        cnt += 1
                if cnt <= 2:
                    melting[i][j] = 1  # 녹을 예정..

    for i in range(n):
        for j in range(n):
            if melting[i][j] and grid[i][j]:
                grid[i][j] -= 1

ans = 0
visited = [[False] * n for i in range(n)]


def bfs(r, c):
    cnt = 0
    q = deque([(r, c)])
    while q:
        r, c = q.pop()
        cnt += 1
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or not grid[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc))
    return cnt


for i in range(n):
    for j in range(n):
        if not visited[i][j] and grid[i][j]:
            visited[i][j] = True
            ans = max(ans, bfs(i, j))

print(sum(map(sum, grid)))
print(ans)
