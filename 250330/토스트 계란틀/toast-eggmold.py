'''
bfs
답이 2000번이 될 수 있는건가?? 안되는 것 같은데 최대 1999인 듯
'''
from collections import deque

n, left, right = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
ans = 0
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(sr, sc):
    global change
    location = []
    q = deque([(sr, sc)])
    sm = 0
    while q:
        r, c = q.popleft()
        location.append((r, c))
        sm += grid[r][c]
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc]:
                continue
            if left <= abs(grid[r][c] - grid[nr][nc]) <= right:
                visited[nr][nc] = 1
                q.append((nr, nc))
    avg = sm // len(location)
    if len(location) > 1:
        change = True
        for r, c in location:
            new_grid[r][c] = avg


for time in range(2000):

    change = False
    visited = [[0] * n for i in range(n)]
    new_grid = [_[:] for _ in grid]
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                bfs(i, j)

    if not change:
        ans = time
        break

    grid = new_grid
print(ans)
