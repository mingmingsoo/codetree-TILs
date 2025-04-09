import copy

n = 4
horse_lst = [0] * 17
grid = [[0] * n for i in range(n)]

for i in range(n):
    tmp = list(map(int, input().split()))
    for j in range(0, 8, 2):
        idx, d = tmp[j], tmp[j + 1]
        grid[i][j // 2] = idx
        horse_lst[idx] = [i, j // 2, d - 1]

sm = grid[0][0]
sr, sc, sd = 0, 0, horse_lst[grid[0][0]][2]
horse_lst[grid[0][0]] = 0
grid[sr][sc] = 0


ans = sm
row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, -1, -1, -1, 0, 1, 1, 1]


def go(r, c, d):
    tmp = []
    for k in range(3):
        nr = r + row[d]
        nc = c + col[d]
        if 0 <= nr < n and 0 <= nc < n:
            if grid[nr][nc]:
                tmp.append((nr, nc))
            r = nr
            c = nc
        else:
            break
    return tmp


def btk(sr, sc, sd, sm):
    global ans, grid, horse_lst
    # 도둑말 이동
    for idx, horse in enumerate(horse_lst):
        if not horse:
            continue
        r, c, d = horse
        move = False
        for k in range(8):
            nr = r + row[d]
            nc = c + col[d]
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) != (sr, sc):
                move = True
                break
            else:
                d = (d + 1) % 8
        if move:
            nr = r + row[d]
            nc = c + col[d]
            if not grid[nr][nc]:
                horse_lst[idx] = [nr, nc, d]
                grid[nr][nc] = idx
                grid[r][c] = 0
            else:
                oidx = grid[nr][nc]
                od = horse_lst[oidx][2]
                grid[nr][nc], grid[r][c] = grid[r][c], grid[nr][nc]
                horse_lst[oidx] = [r, c, od]
                horse_lst[idx] = [nr, nc, d]

    grid_origin = [_[:] for _ in grid]
    horse_lst_origin = copy.deepcopy(horse_lst)

    lst = go(sr, sc, sd)
    if not lst:
        ans = max(ans, sm)
        return
    else:
        for nsr, nsc in lst:
            eat = grid[nsr][nsc]
            nsd = horse_lst[grid[nsr][nsc]][2]
            horse_lst[grid[nsr][nsc]] = 0
            grid[nsr][nsc] = 0
            btk(nsr, nsc, nsd, sm + eat)
            grid = [_[:] for _ in grid_origin]
            horse_lst = copy.deepcopy(horse_lst_origin)


btk(sr, sc, sd, sm)
print(ans)
