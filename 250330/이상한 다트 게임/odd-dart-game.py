'''
시간복잡도
명령수 50* 회전횟수 m 50* 인접찾기 n,m 50*50
50^4
'''
from collections import deque

n, m, order_num = map(int, input().split())
grid = [deque(map(int, input().split())) for i in range(n)]

for order in range(order_num):
    x, d, ro = map(int, input().split())
    if d == 0:
        d = 1
    else:
        d = -1
    ro *= d

    for i in range(x - 1, n, x):  # 배수만..
        grid[i].rotate(ro)


    # 인접 찾기
    is_close = False
    close = [[0] * m for i in range(n)]
    # 가로 찾자
    for i in range(n):
        for j in range(-1, m - 1, 1):
            if grid[i][j] and grid[i][j] == grid[i][j + 1]:
                close[i][j] = close[i][j + 1] = 1
                is_close = True
    # 세로 찾자
    for j in range(m):
        for i in range(n - 1):
            if grid[i][j] and grid[i][j] == grid[i + 1][j]:
                close[i][j] = close[i + 1][j] = 1
                is_close = True

    if is_close:
        for i in range(n):
            for j in range(m):
                if close[i][j]:
                    grid[i][j] = 0
    else:
        cnt = 0
        sm = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j]:
                    cnt += 1
                    sm += grid[i][j]

        for i in range(n):
            for j in range(m):
                if grid[i][j] and grid[i][j] > sm // cnt:
                    grid[i][j] -= 1
                elif grid[i][j] and grid[i][j] < sm // cnt:
                    grid[i][j] += 1

print(sum(map(sum, grid)))
