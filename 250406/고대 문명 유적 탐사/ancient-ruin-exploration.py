'''
문제 설명
    1. 격자 선택
    2. bfs 진행 (while)
'''
from collections import deque

n = 5
turn, fn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
fill = list(map(int, input().split()))


def rotation(small_grid):
    ro = [[0] * 3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            ro[i][j] = small_grid[3 - j - 1][i]
    return ro


row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs():
    total = 0
    visited = [[False] * n for i in range(n)]
    lo = []
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                ele = 0
                visited[i][j] = True
                q = deque([(i, j)])
                ele_lo = []
                while q:
                    qr, qc = q.popleft()
                    ele_lo.append((qr, qc))
                    ele += 1
                    for k in range(4):
                        nqr = qr + row[k]
                        nqc = qc + col[k]
                        if not (0 <= nqr < n and 0 <= nqc < n) or visited[nqr][nqc] or grid[nqr][nqc] != grid[i][j]:
                            continue
                        visited[nqr][nqc] = True
                        q.append((nqr, nqc))
                if ele >= 3:
                    lo.extend(ele_lo)
                    total += ele

    return total, lo


for t in range(turn):
    ans = 0
    sel = []

    for r in range(3):
        for c in range(3):
            grid_origin = [_[:] for _ in grid]
            small_grid = [_[c:c + 3] for _ in grid[r:r + 3]]
            ro90 = rotation(small_grid)
            for i in range(3):
                for j in range(3):
                    grid[i + r][j + c] = ro90[i][j]
            cnt, location = bfs()

            if cnt:
                sel.append((-cnt, 90, c, r,  [_[:] for _ in grid]))

            ro180 = rotation(ro90)
            for i in range(3):
                for j in range(3):
                    grid[i + r][j + c] = ro180[i][j]
            cnt, location = bfs()

            if cnt:
                sel.append((-cnt, 180, c, r,  [_[:] for _ in grid]))

            ro270 = rotation(ro180)
            for i in range(3):
                for j in range(3):
                    grid[i + r][j + c] = ro270[i][j]
            cnt, location = bfs()

            if cnt:
                sel.append((-cnt, 270, c, r,  [_[:] for _ in grid]))

            grid = [_[:] for _ in grid_origin]

    if not sel:
        break
    sel.sort()

    score, degree, cc, rr, new_grid = sel[0]
    grid = new_grid

    while True:
        cnt, location = bfs()
        if cnt:
            ans += cnt
            for r, c in location:
                grid[r][c] = 0
        else:
            break
        for j in range(n):
            for i in range(n - 1, -1, -1):
                if not grid[i][j]:
                    grid[i][j] = fill.pop(0)
    print(ans, end = " ")
