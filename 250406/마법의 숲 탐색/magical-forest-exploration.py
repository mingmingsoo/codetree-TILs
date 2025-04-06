'''
문제설명
    1. 골렘 이동
    2. 정령 탈출
중심좌표 r,c
'''
from collections import deque

n, m, pn = map(int, input().split())
n += 3
grid = [[0] * m for i in range(n)]


def oob(r, c):
    if 0 <= r < n and 0 <= c < m:
        return True
    return False


def down():
    global r
    # 중심 r,c
    #       왼 r,c-1 하 r+1,c 우 r,c+1
    # 그 밑   r+1,c-1  r+2,c   r+1,c+1
    while oob(r + 1, c - 1) and oob(r + 2, c) and oob(r + 1, c + 1) and not grid[r + 1][c - 1] and not grid[r + 2][
        c] and not grid[r + 1][c + 1]:
        r += 1


row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]


def left():
    global r, c, d
    # 중심 r,c
    #       위왼 r-1,c-1 왼왼 r,c-2 아왼 r+1,c-1
    #                       r+1,c-2    r+2,c-1
    if oob(r - 1, c - 1) and oob(r, c - 2) and oob(r + 1, c - 1) and oob(r + 1, c - 2) and oob(r + 2, c - 1) and not \
            grid[r - 1][c - 1] and not grid[r][c - 2] and not grid[r + 1][c - 1] and not grid[r + 1][c - 2] and not \
            grid[r + 2][c - 1]:
        d = (d - 1) % 4
        r += 1
        c -= 1
        return True
    return False


def right():
    global r, c, d
    # 중심 r,c
    #       위오 r-1,c+1 오오 r,c+2  아오 r+1,c+1
    #                       r+1,c+2     r+2,c+1
    if oob(r - 1, c + 1) and oob(r, c + 2) and oob(r + 1, c + 1) and oob(r + 1, c + 2) and oob(r + 2, c + 1) and not \
            grid[r - 1][c + 1] and not grid[r][c + 2] and not grid[r + 1][c + 1] and not grid[r + 1][c + 2] and not \
            grid[r + 2][c + 1]:
        d = (d + 1) % 4
        r += 1
        c += 1
        return True
    return False


ans = 0


def bfs(sr, sc):
    visited = [[False] * m for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, grid[sr][sc])])
    maxi = sr
    while q:
        r, c, p = q.popleft()
        maxi = max(maxi, r)
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not oob(nr, nc) or visited[nr][nc]:
                continue
            if abs(grid[nr][nc]) == p:
                visited[nr][nc] = True
                q.append((nr, nc, abs(grid[nr][nc])))
            if grid[r][c] < 0 and grid[nr][nc]:
                visited[nr][nc] = True
                q.append((nr,nc,abs(grid[nr][nc])))


    return maxi


for p in range(pn):
    c, d = map(int, input().split())
    c -= 1
    r = 1
    while True:
        down()
        move = False
        if left():
            move = True
        if right():
            move = True
        if not move:
            break
    if r <= 3:
        grid = [[0] * m for i in range(n)]
        continue

    # 흔적 남기기
    grid[r][c] = grid[r + 1][c] = grid[r - 1][c] = grid[r][c - 1] = grid[r][c + 1] = p + 1
    if d == 0:
        grid[r - 1][c] = -(p + 1)
    elif d == 2:
        grid[r + 1][c] = -(p + 1)
    elif d == 1:
        grid[r][c + 1] = -(p + 1)
    elif d == 3:
        grid[r][c - 1] = -(p + 1)
    # print("---------------")
    # for i in range(n):
    #     for j in range(m):
    #         if grid[i][j]<0:
    #             print("x", end = " ")
    #         else:
    #             print(grid[i][j], end= " ")
    #     print()
    maxi = bfs(r, c)
    # print(maxi-2)
    ans += maxi-2
print(ans)