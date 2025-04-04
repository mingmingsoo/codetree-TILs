'''
s를 2(r-1) 로 나눈 나머지로 변환
'''
n, m, virus = map(int, input().split())
grid = [[0] * m for i in range(n)]
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
change_d = [1, 0, 3, 2]
for v in range(virus):
    r, c, s, d, size = map(int, input().split())
    r -= 1
    c -= 1
    d -= 1
    if d in (0, 1):
        s %= 2 * (n - 1)
    else:
        s %= 2 * (m - 1)
    grid[r][c] = (v, s, d, size)

eat = 0


def myprint(grid):
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                print(grid[i][j][3], end=" ")
            else:
                print(0, end=" ")
        print()

# print("------------시작-----------------")
# myprint(grid)
for j in range(m):
    # 1. 곰팡이 채취
    for i in range(n):
        if grid[i][j]:
            eat += grid[i][j][3]
            grid[i][j] = 0
            break
    # print(eat)
    # print("------------먹고난 후-----------------",j)
    # myprint(grid)
    # 2. 곰팡이 이동
    new_grid = [[0] * m for i in range(n)]
    for ii in range(n):
        for jj in range(m):
            if grid[ii][jj]:
                num, s, d, size = grid[ii][jj]
                r, c = ii, jj
                for ss in range(s):
                    nr = r + row[d]
                    nc = c + col[d]
                    if not (0 <= nr < n and 0 <= nc < m):
                        d = change_d[d]
                    nr = r + row[d]
                    nc = c + col[d]
                    r = nr
                    c = nc
                if not new_grid[r][c]:
                    new_grid[r][c] = (num,s,d,size)
                else:
                    if new_grid[r][c][3] < size:
                        new_grid[r][c] = (num, s, d, size)

    # print("------------이동 후-----------------")
    # myprint(new_grid)
    grid = new_grid

print(eat)