dragon_num = int(input())

grid = [[0] * 101 for i in range(101)]
row = [0, -1, 0, 1]
col = [1, 0, -1, 0]
for dragon in range(dragon_num):
    r, c, d, g = map(int, input().split())
    # 0세대 기록
    d_arr = [d]
    lo_arr = [(r, c)]

    for _ in range(g):
        for l in range(len(d_arr) - 1, -1, -1):
            d_arr.append((d_arr[l] + 1) % 4)
    for dd in d_arr:
        x, y = lo_arr[-1]
        nx = x + row[dd]
        ny = y + col[dd]
        lo_arr.append((nx, ny))
    for x, y in lo_arr:
        grid[x][y] = 1

ans = 0
for i in range(100):
    for j in range(100):
        if grid[i][j] and grid[i + 1][j] and grid[i][j + 1] and grid[i + 1][j + 1]:
            ans += 1
print(ans)