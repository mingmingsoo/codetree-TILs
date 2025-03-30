from collections import deque

n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

for i in range(n):
    for j in range(n):
        if grid[i][j] == 9:
            r, c, eat, level = i, j, 0, 2
            grid[r][c] = 0

time = 0
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(r, c):
    visited = [[False] * n for i in range(n)]
    visited[r][c] = True
    q = deque([(r, c, 0)])
    while q:
        for qs in range(len(q)):
            r, c, dist = q.popleft()
            for k in range(4):
                nr = r + row[k]
                nc = c + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] > level:
                    continue
                if 0< grid[nr][nc] < level:
                    monsters.append((dist + 1, nr, nc))
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
        if monsters:
            return


while True:

    monsters = []
    bfs(r, c)
    if not monsters:
        break
    monsters.sort()
    dist, mr, mc = monsters[0]
    time+=dist
    grid[mr][mc] = 0
    r, c = mr, mc
    eat += 1
    if eat == level:
        level += 1
        eat = 0

print(time)
