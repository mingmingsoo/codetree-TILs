'''
dfs+하드코딩
4 5
0 0 0 0 0
0 0 0 0 0
0 0 1 1 1
0 0 0 1 0


5 4
0 0 0 0
0 0 0 0
0 0 0 1
0 0 1 1
0 0 0 1

5 4
0 0 0 0
0 0 0 0
0 0 1 0
0 0 1 1
0 0 1 0

5 4
0 0 0 0
0 0 0 0
1 0 0 0
1 1 0 1
1 0 0 0
'''

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
ans = 0

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def dfs(r, c, sm, depth):
    global ans
    if depth == 3:
        ans = max(ans, sm)
        return
    visited[r][c] = True

    for k in range(4):
        nr = r + row[k]
        nc = c + col[k]
        if not (0 <= nr < n and 0 <= nc < m) or visited[nr][nc]:
            continue
        dfs(nr, nc, sm + grid[nr][nc], depth + 1)
    visited[r][c] = False


visited = [[False] * m for i in range(n)]
for i in range(n):
    for j in range(m):
        dfs(i, j, grid[i][j], 0)

# ㅏ ㅓ
for i in range(n - 2):
    for j in range(m):
        sm = grid[i][j] + grid[i + 1][j] + grid[i + 2][j]
        sm1 = sm2 = sm
        if j > 0:
            sm1 += grid[i + 1][j - 1]
        if j < m - 1:
            sm2 += grid[i + 1][j + 1]
        ans = max(ans, sm1, sm2)
# ㅜ ㅗ
for i in range(n):
    for j in range(m - 2):
        sm = grid[i][j] + grid[i][j + 1] + grid[i][j + 2]
        sm1 = sm2 = sm
        if i > 0:
            sm1 += grid[i - 1][j + 1]
        if i < n - 1:
            sm2 += grid[i + 1][j + 1]
        ans = max(ans, sm1, sm2)
print(ans)