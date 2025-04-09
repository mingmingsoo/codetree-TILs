from collections import deque

p, on = map(int, input().split())
n = 2 ** p
grid = [list(map(int, input().split())) for i in range(n)]

order_lst = list(map(int, input().split()))


def rotation(sr, sc):
    small_grid = [_[sc:sc + m] for _ in grid[sr:sr + m]]
    # 얘를 4등분해
    small_grid1 = [_[:m // 2] for _ in small_grid[: m // 2]]
    small_grid2 = [_[m // 2:m] for _ in small_grid[:m // 2]]
    small_grid3 = [_[:m // 2] for _ in small_grid[m // 2:m]]
    small_grid4 = [_[m // 2:m] for _ in small_grid[m // 2:m]]

    for i in range(m // 2):
        for j in range(m // 2):
            grid[i + sr][j + sc] = small_grid3[i][j]
    for i in range(m // 2):
        for j in range(m // 2):
            grid[i + sr][j + sc + m // 2] = small_grid1[i][j]
    for i in range(m // 2):
        for j in range(m // 2):
            grid[i + sr + m // 2][j + sc] = small_grid4[i][j]
    for i in range(m // 2):
        for j in range(m // 2):
            grid[i + sr + m // 2][j + sc + m // 2] = small_grid2[i][j]


row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]

for l in order_lst:
    m = 2 ** l
    # 잘라
    for i in range(0, n, m):
        for j in range(0, n, m):
            rotation(i, j)

    delete = set()
    for i in range(n):
        for j in range(n):
            ice = 0
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
                    ice += 1

            if ice < 3:
                delete.add((i, j))
    for r, c in delete:
        if grid[r][c]:
            grid[r][c] -= 1

# 최대 군집 갯수
maxi = 0
visited = [[False] * n for i in range(n)]
for i in range(n):
    for j in range(n):
        if grid[i][j] and not visited[i][j]:
            visited[i][j] = True
            cnt = 0
            q = deque([(i, j)])
            while q:
                r, c = q.popleft()
                cnt += 1
                for k in range(4):
                    nr = r + row[k]
                    nc = c + col[k]
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] and not visited[nr][nc]:
                        visited[nr][nc] = True
                        q.append((nr, nc))
            maxi = max(maxi, cnt)

print(sum(map(sum, grid)))
print(maxi)
