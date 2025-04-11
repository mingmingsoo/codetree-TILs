n, pn, turn = map(int, input().split())
tmp = [list(map(int, input().split())) for i in range(n)]
grid = [[[] for i in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        if tmp[i][j]:
            grid[i][j].append(tmp[i][j])
player_grid = [[0] * n for i in range(n)]
player_lst = [0] * (pn + 1)

for p in range(1, pn + 1):
    r, c, d, s = map(int, input().split())
    player_grid[r - 1][c - 1] = p
    player_lst[p] = [r - 1, c - 1, d, s, 0]
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
score = [0] * (pn + 1)


def battle(win_idx, lose_idx):
    lr, lc, ld, ls, lg = player_lst[lose_idx]
    if lg:
        grid[lr][lc].append(lg)
        lg = 0
    for k in range(4):
        nlr = lr + row[ld]
        nlc = lc + col[ld]
        if 0 <= nlr < n and 0 <= nlc < n and not player_grid[nlr][nlc]:
            lr = nlr
            lc = nlc
            break
        else:
            ld = (ld + 1) % 4
    if grid[lr][lc]:
        other_gun = max(grid[lr][lc])
        lg = other_gun
        grid[lr][lc].remove(other_gun)
    player_lst[lose_idx] = [lr, lc, ld, ls, lg]
    player_grid[lr][lc] = lose_idx

    wr, wc, wd, ws, wg = player_lst[win_idx]
    if grid[wr][wc]:
        other_gun = max(grid[nr][nc])
        if other_gun > wg:
            grid[nr][nc].remove(other_gun)
            if wg:
                grid[nr][nc].append(wg)
            wg = other_gun
    player_lst[win_idx] = [wr, wc, wd, ws, wg]
    player_grid[wr][wc] = win_idx


for t in range(turn):

    for idx, player in enumerate(player_lst):
        if idx == 0:
            continue
        r, c, d, s, gun = player
        nr = r + row[d]
        nc = c + col[d]
        if not (0 <= nr < n and 0 <= nc < n):
            d = (d + 2) % 4
        nr = r + row[d]
        nc = c + col[d]

        if not player_grid[nr][nc]:  # 아무도 업송
            player_grid[r][c] = 0
            player_grid[nr][nc] = idx
            if grid[nr][nc]:  # 총 이쓰면
                other_gun = max(grid[nr][nc])
                if other_gun > gun:
                    grid[nr][nc].remove(other_gun)
                    if gun:
                        grid[nr][nc].append(gun)
                    gun = other_gun
            player_lst[idx] = [nr, nc, d, s, gun]

        else:  # 쌈 떠
            player_grid[r][c] = 0  # 빈 공간 만들어쥬공..
            player_lst[idx] = [nr, nc, d, s, gun]  # 일단 갱신 해주공...
            oidx = player_grid[nr][nc]
            xr, xc, xd, xs, xgun = player_lst[oidx]  # 나랑 쌈 뜰애
            win_idx, lose_idx = 0, 0
            if s + gun > xs + xgun:
                win_idx = idx
                lose_idx = oidx
            if s + gun == xs + xgun:
                if s > xs:
                    win_idx = idx
                    lose_idx = oidx
                else:
                    win_idx = oidx
                    lose_idx = idx
            if s + gun < xs + xgun:
                win_idx = oidx
                lose_idx = idx
            score[win_idx] += abs(s + gun - xs - xgun)
            battle(win_idx, lose_idx)

print(*score[1:])
