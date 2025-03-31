import copy

n = 4
grid = [[0] * n for i in range(n)]
thief_lst = [0] * 17

for i in range(n):
    tmp = list(map(int, input().split()))
    for j in range(0, 8, 2):
        num, d = tmp[j], tmp[j + 1]
        grid[i][j // 2] = num
        thief_lst[num] = [i, j // 2, d - 1]
ans = 0
pr = pc = pd = 0  # 술래 위치, 방향
ans += grid[pr][pc]
pd = thief_lst[grid[pr][pc]][2]

sm = ans
thief_lst[grid[pr][pc]] = 0
grid[pr][pc] = 0
row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, -1, -1, -1, 0, 1, 1, 1]



def go(pr, pc, pd):
    lo = []
    for k in range(3):
        nr = pr + row[pd]
        nc = pc + col[pd]
        if not (0 <= nr < n and 0 <= nc < n):
            break
        if grid[nr][nc]:
            lo.append((nr, nc))
        pr = nr
        pc = nc
    return lo


def btk(pr, pc, pd, sm):
    global ans, grid, thief_lst

    for idx, thief in enumerate(thief_lst):
        if thief == 0:
            continue
        r, c, d = thief_lst[idx]
        for k in range(8):
            nr = r + row[d]
            nc = c + col[d]
            if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) == (pr, pc):
                d = (d + 1) % 8
            else:
                break
        nr = r + row[d]
        nc = c + col[d]
        oidx = grid[nr][nc]
        grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]

        thief_lst[idx][0] = nr
        thief_lst[idx][1] = nc
        thief_lst[idx][2] = d

        if oidx:
            thief_lst[oidx][0] = r
            thief_lst[oidx][1] = c
    # 이동
    grid_origin = [_[:] for _ in grid]
    thief_lst_origin = copy.deepcopy(thief_lst)

    location = go(pr, pc, pd)
    if not location:
        ans = max(ans, sm)
        return
    else:
        for r, c in location:
            ele_sm = grid[r][c]
            d = thief_lst[grid[r][c]][2]
            thief_lst[grid[r][c]] = 0
            grid[r][c] = 0


            btk(r, c, d, sm + ele_sm)
            grid = [_[:] for _ in grid_origin]
            thief_lst = copy.deepcopy(thief_lst_origin)


btk(pr, pc, pd, sm)
print(ans)
