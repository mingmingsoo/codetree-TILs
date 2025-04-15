from collections import deque

n, turn = map(int, input().split())
color_grid = [list(input()) for i in range(n)]
energy_grid = [list(map(int, input().split())) for i in range(n)]
change = {"T": 1, "C": 2, "M": 3}
for i in range(n):
    for j in range(n):
        color_grid[i][j] = change[color_grid[i][j]]

color_dict = {(1, 2): 6, (1, 3): 5, (1, 4): 7, (1, 5): 5, (1, 6): 6, (1, 7): 7,
              (2, 3): 4, (2, 4): 4, (2, 5): 7, (2, 6): 6, (2, 7): 7,
              (3, 4): 4, (3, 5): 5, (3, 6): 7, (3, 7): 7,
              (4, 5): 7, (4, 6): 7, (4, 7): 7,
              (5, 6): 7, (5, 7): 7,
              (6, 7): 7}
row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]


def bfs(r, c):
    my_color = color_grid[r][c]
    location = []
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        location.append((-energy_grid[r][c], (r, c)))
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if 0 <= nr < n and 0 <= nc < n and not v[nr][nc] and color_grid[nr][nc] == my_color:
                q.append((nr, nc))
                v[nr][nc] = 1
    location.sort()
    be, bcrd = location[0]
    br, bc = bcrd
    energy_grid[br][bc] += len(location) - 1
    for i in range(1, len(location)):
        e, crd = location[i]
        r, c = crd
        energy_grid[r][c] -= 1
    return br, bc


for t in range(1, turn + 1):

    for i in range(n):
        for j in range(n):
            energy_grid[i][j] += 1
    v = [[0] * n for i in range(n)]
    shoot_grid = [[False] * n for i in range(n)]
    lst = []
    for i in range(n):
        for j in range(n):
            if not v[i][j]:
                v[i][j] = 1
                r, c = bfs(i, j)
                shoot_grid[r][c] = True
                if 1 <= color_grid[r][c] <= 3:
                    lst.append((1, -energy_grid[r][c], (r, c)))
                elif 4 <= color_grid[r][c] <= 6:
                    lst.append((2, -energy_grid[r][c], (r, c)))
                else:
                    lst.append((3, -energy_grid[r][c], (r, c)))
    lst.sort()
    for o, e, lo in lst:
        r, c = lo
        if not shoot_grid[r][c]:
            continue
        e *= -1
        d = e % 4
        power = e - 1
        energy_grid[r][c] = 1
        my_color = color_grid[r][c]
        q = deque([(r, c, power)])
        while q:
            qr, qc, qp = q.popleft()
            nqr = qr + row[d]
            nqc = qc + col[d]
            if not (0 <= nqr < n and 0 <= nqc < n):
                break
            if (color_grid[nqr][nqc] == my_color):
                q.append((nqr, nqc, qp))
            else:
                shoot_grid[nqr][nqc] = False
                if qp > energy_grid[nqr][nqc]:
                    next_qp = qp - (energy_grid[nqr][nqc] + 1)
                    energy_grid[nqr][nqc] += 1
                    color_grid[nqr][nqc] = my_color
                    if next_qp > 0:
                        q.append((nqr, nqc, next_qp))
                else:
                    energy_grid[nqr][nqc] += qp
                    tmp = [my_color, color_grid[nqr][nqc]]
                    tmp.sort()
                    color_grid[nqr][nqc] = color_dict[tuple(tmp)]
    score = [0] * 8
    for i in range(n):
        for j in range(n):
            score[color_grid[i][j]] += energy_grid[i][j]
    score.reverse()
    print(*score[:7])
