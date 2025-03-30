'''
대각선이 될 수 있는 범위는 1~n-1
대각선의 길이도 1~n-1
'''
n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]
row = [1, 1]
col = [-1, 1]

ans = int(1e9)


def cal(i, j, d1, d2):
    global ans
    area = [[0] * n for i in range(n)]
    r, c = i, j
    for d in range(d1):
        area[r][c] = 5
        nr = r + row[0]
        nc = c + col[0]
        r = nr
        c = nc
    for d in range(d2 + 1):
        area[r][c] = 5
        nr = r + row[1]
        nc = c + col[1]
        r = nr
        c = nc

    r, c = i, j
    for d in range(d2):
        area[r][c] = 5
        nr = r + row[1]
        nc = c + col[1]
        r = nr
        c = nc

    for d in range(d1):
        area[r][c] = 5
        nr = r + row[0]
        nc = c + col[0]
        r = nr
        c = nc

    for r in range(i + d1):
        for c in range(j + 1):
            if area[r][c] != 5:
                area[r][c] = 1
            else:
                break

    for r in range(i + d2 + 1):
        for c in range(n - 1, j, -1):
            if area[r][c] != 5:
                area[r][c] = 2
            else:
                break

    for r in range(i + d1, n):
        for c in range(j):
            if area[r][c] != 5:
                area[r][c] = 3
            else:
                break

    for r in range(i + d2 + 1, n):
        for c in range(n - 1, j-1, -1):
            if area[r][c] != 5:
                area[r][c] = 4
            else:
                break

    one, two, three, four, five = 0, 0, 0, 0, 0
    for i in range(n):
        for j in range(n):
            if area[i][j] == 1:
                one += grid[i][j]
            elif area[i][j] == 2:
                two += grid[i][j]
            elif area[i][j] == 3:
                three += grid[i][j]
            elif area[i][j] == 4:
                four += grid[i][j]
            else:
                five += grid[i][j]

    tmp = [one, two, three, four, five]
    ans = min(max(tmp) - min(tmp), ans)


for i in range(n - 1):
    for j in range(n - 1):
        # 얘가 윗점이 될 거임
        for d1 in range(1, n - 1):
            for d2 in range(1, n - 1):
                # 대각선 길이
                if j - d1 >= 0 and j + d2 < n and i + d1 + d2 < n:
                    cal(i, j, d1, d2)
print(ans)