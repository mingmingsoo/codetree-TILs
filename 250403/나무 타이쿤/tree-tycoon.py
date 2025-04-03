n, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
nutrition = set([(n - 1, 0), (n - 1, 1), (n - 2, 0), (n - 2, 1)])

row = [0, -1, -1, -1, 0, 1, 1, 1]
col = [-1, -1, 0, 1, 1, 1, 0, -1]

for t in range(time):
    d, l = map(int, input().split())
    d -= 1
    new_nu = set()
    for r, c in nutrition:
        nr = (r + row[d] * l) % n
        nc = (c + col[d] * l) % n
        grid[nr][nc] += 1
        new_nu.add((nr, nc))
    plus_grid = [[0] * n for i in range(n)]

    for r, c in new_nu:
        cnt = 0
        for k in (1, 3, 5, 7):
            nr = r + row[k]
            nc = c + col[k]
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
                cnt += 1
        plus_grid[r][c] += cnt

    for i in range(n):
        for j in range(n):
            if plus_grid[i][j]:
                grid[i][j] += plus_grid[i][j]

    new_nutrition = set()
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= 2 and (i, j) not in new_nu:
                grid[i][j] -= 2
                new_nutrition.add((i, j))

    nutrition = new_nutrition

print(sum(map(sum, grid)))
