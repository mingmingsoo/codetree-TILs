'''
플레이어 정보 1차원 배열로도 관리

'''


def battle(win, lose):
    # 진 사람 로직
    lr, lc, ld, lp, lg = player_info[lose]
    if lg:
        grid[lr][lc].append(lg)
        lg = 0
    for k in range(4):
        if not (0 <= lr + row[ld] < n and 0 <= lc + col[ld] < n) or player_grid[lr + row[ld]][lc + col[ld]] != -1:
            ld = (ld + 1) % 4
        else:
            break
    nlr = lr + row[ld]
    nlc = lc + col[ld]
    if grid[nlr][nlc]:
        other_gun = max(grid[nlr][nlc])
        lg = other_gun
        grid[nlr][nlc].remove(lg)
    player_info[lose] = (nlr, nlc, ld, lp, lg)
    player_grid[nlr][nlc] = lose

    # 이긴 사람 로직
    wr, wc, wd, wp, wg = player_info[win]
    if grid[wr][wc]:
        other_gun = max(grid[wr][wc])
        if other_gun > wg:
            grid[wr][wc].append(wg)
            wg = other_gun
            grid[wr][wc].remove(wg)
    player_info[win] = (wr, wc, wd, wp, wg)
    player_grid[wr][wc] = win


def move():
    for idx, player in enumerate(player_info):
        r, c, d, power, gun = player
        if not (0 <= r + row[d] < n and 0 <= c + col[d] < n):
            d = (d + 2) % 4
        nr = r + row[d]
        nc = c + col[d]
        if player_grid[nr][nc] == -1:  # 싸움 안함!
            if grid[nr][nc]:
                other_gun = max(grid[nr][nc])
                if gun < other_gun:
                    grid[nr][nc].remove(other_gun)
                    grid[nr][nc].append(gun)
                    gun = other_gun
            player_grid[nr][nc] = idx
            player_grid[r][c] = -1
            player_info[idx] = (nr, nc, d, power, gun)
        else:  # 싸움 함!
            player_info[idx] = (nr, nc, d, power, gun)
            o_idx = player_grid[nr][nc]
            o_r, o_c, o_d, o_power, o_gun = player_info[o_idx]  # 누구랑 싸울건데
            my_score = power + gun
            o_score = o_power + o_gun
            if my_score > o_score:
                win = idx
                lose = o_idx
            elif my_score == o_score:
                if power > o_power:
                    win = idx
                    lose = o_idx
                else:
                    win = o_idx
                    lose = idx
            else:
                win = o_idx
                lose = idx
            player_grid[r][c] = -1  # 일단 빈공간은 맞음
            ans[win] += abs(my_score - o_score)
            battle(win, lose)


n, player_num, time = map(int, input().split())
tmp = [list(map(int, input().split())) for i in range(n)]

grid = [[[] for i in range(n)] for i in range(n)]
player_grid = [[-1] * n for i in range(n)]
player_info = []
for p in range(player_num):
    r, c, d, power = map(int, input().split())
    player_grid[r - 1][c - 1] = p
    player_info.append((r - 1, c - 1, d, power, 0))
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]

for i in range(n):
    for j in range(n):
        if tmp[i][j]:
            grid[i][j].append(tmp[i][j])

ans = [0] * player_num

for t in range(time):
    move()
print(*ans)
