'''
한번에 가보자이
규칙성 2*(r/c-1)

승용이가 채취한 곰팡이 사이즈 합 출력
'''

n, m, vn = map(int, input().split())
grid = [[0] * m for i in range(n)]
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
change = [1, 0, 3, 2]
for v in range(vn):
    r, c, s, d, b = map(int, input().split())
    r -= 1
    c -= 1
    d -= 1
    if d in (0, 1):
        grid[r][c] = (s % (2 * (n - 1)), d, b)
    else:
        grid[r][c] = (s % (2 * (m - 1)), d, b)
ans = 0


# 1. 승용이 열 탐색
def myprint():
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                print(grid[i][j][2], end=" ")
            else:
                print(0, end=" ")
        print()


for j in range(m):

    # 2. 가장 빨리 발견하는 곰팡이 채취
    for i in range(n):
        if grid[i][j]:
            ans += grid[i][j][2]
            grid[i][j] = 0
            break
    # 3. 곰팡이 이동 -> new_grid 필요
    new_grid = [[0] * m for i in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                s, d, b = grid[i][j]
                r, c = i, j
                for ss in range(s):
                    nr = r + row[d]
                    nc = c + col[d]
                    if not (0 <= nr < n and 0 <= nc < m):
                        d = change[d]
                    nr = r + row[d]
                    nc = c + col[d]
                    r = nr
                    c = nc

                if not new_grid[r][c]:
                    new_grid[r][c] = (s, d, b)
                else:
                    if new_grid[r][c][2] < b:
                        new_grid[r][c] = (s, d, b)

    grid = new_grid

print(ans)