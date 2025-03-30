'''

'''

n, m, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

air1 = (0, 0)
air2 = (0, 0)


def find():
    global air1, air2
    for i in range(n):
        if grid[i][0] == -1:
            air1 = (i, 0)
            air2 = (i + 1, 0)
            return


find()

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def spread():
    for i in range(n):
        for j in range(m):
            if grid[i][j] > 0:
                rnd = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if not (0 <= nr < n and 0 <= nc < m) or grid[nr][nc] < 0:
                        continue
                    rnd += 1
                munji = grid[i][j] // 5
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if not (0 <= nr < n and 0 <= nc < m) or grid[nr][nc] < 0:
                        continue
                    plus_grid[nr][nc] += munji
                plus_grid[i][j] -= munji * rnd


def rotation():
    # 위에 반시계
    for i in range(air1[0], 0, -1):
        grid[i][air1[1]], grid[i - 1][air1[1]] = grid[i - 1][air1[1]], grid[i][air1[1]]
    for j in range(m - 1):
        grid[0][j], grid[0][j + 1] = grid[0][j + 1], grid[0][j]
    for i in range(air1[0]):
        grid[i][m - 1], grid[i + 1][m - 1] = grid[i + 1][m - 1], grid[i][m - 1]
    for j in range(m - 1, 0, -1):
        grid[air1[0]][j], grid[air1[0]][j - 1] = grid[air1[0]][j - 1], grid[air1[0]][j]
    grid[air1[0]][air1[1] + 1] = 0
    grid[air1[0]][air1[1]] = -1

    # 아래 시계
    for i in range(air2[0], n - 1):
        grid[i][air2[1]], grid[i + 1][air2[1]] = grid[i + 1][air2[1]], grid[i][air2[1]]
    for j in range(m - 1):
        grid[n - 1][j], grid[n - 1][j + 1] = grid[n - 1][j + 1], grid[n - 1][j]
    for i in range(n - 1, air2[0], -1):
        grid[i][m - 1], grid[i - 1][m - 1] = grid[i - 1][m - 1], grid[i][m - 1]
    for j in range(m - 1, 0, -1):
        grid[air2[0]][j], grid[air2[0]][j - 1] = grid[air2[0]][j - 1], grid[air2[0]][j]
    grid[air2[0]][air2[1] + 1] = 0
    grid[air2[0]][air2[1]] = -1


for t in range(time):
    plus_grid = [[0] * m for i in range(n)]
    spread()

    for i in range(n):
        for j in range(m):
            grid[i][j] += plus_grid[i][j]

    rotation()

print(sum(map(sum, grid)) + 2)
