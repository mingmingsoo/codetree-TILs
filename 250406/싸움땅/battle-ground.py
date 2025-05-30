'''
문제 설명
    1. 플레이어 순차 이동
    2. 플레이어 없으면 총먹어
                있으면 싸움

입력
    맵n, 플레이어 수 m, 턴 수 turn
    총 정보(맵)
    플레이어 정보 r,c,d,s
필요한 변수
player_lst = [위치,방향,능력치,총]
player_grid = [넘버만]
gun_grid = 3차원
'''

n, pm, turn = map(int, input().split())
tmp = [list(map(int, input().split())) for i in range(n)]
gun_grid = [[[] for i in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        if tmp[i][j]:
            gun_grid[i][j].append(tmp[i][j])
player_lst = [0]
player_grid = [[0] * n for i in range(n)]
for _ in range(pm):
    r, c, d, s = map(int, input().split())
    player_lst.append([r - 1, c - 1, d, s, 0])
    player_grid[r - 1][c - 1] = _ + 1

score = [0] * (pm + 1)
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]


def move(win_idx, lose_idx, x, y):
    # 진 플레이어 이동
    _, _, d, s, gun = player_lst[lose_idx]
    if gun:
        gun_grid[x][y].append(gun)
        gun = 0
    for k in range(4):
        nr = x + row[d]
        nc = y + col[d]
        if 0 <= nr < n and 0 <= nc < n and player_grid[nr][nc] == 0:
            break
        else:
            d = (d + 1) % 4
    if gun_grid[nr][nc]:
        gun = max(gun_grid[nr][nc])
        gun_grid[nr][nc].remove(gun)
    player_lst[lose_idx] = [nr, nc, d, s, gun]
    player_grid[nr][nc] = lose_idx

    # 이긴 플레이어 이동
    _, _, d, s, gun = player_lst[win_idx]
    if gun_grid[x][y]:
        other_gun = max(gun_grid[x][y])
        if other_gun > gun:
            gun_grid[x][y].remove(other_gun)
            if gun:
                gun_grid[x][y].append(gun)
            gun = other_gun
    player_lst[win_idx] = [x, y, d, s, gun]
    player_grid[x][y] = win_idx


for t in range(turn):
    for p in range(1, pm + 1):
        r, c, d, s, gun = player_lst[p]
        nr = r + row[d]
        nc = c + col[d]
        if not (0 <= nr < n and 0 <= nc < n):
            d = (d + 2) % 4
        nr = r + row[d]
        nc = c + col[d]
        player_grid[r][c] = 0
        player_lst[p][2] = d
        if not player_grid[nr][nc]:  # 빈 곳
            other_gun = 0
            if gun_grid[nr][nc]:
                other_gun = max(other_gun, max(gun_grid[nr][nc]))
            if other_gun > gun:
                if gun > 0:
                    gun_grid[nr][nc].append(gun)
                gun_grid[nr][nc].remove(other_gun)
                gun = other_gun
            player_grid[nr][nc] = p
            player_lst[p] = [nr, nc, d, s, gun]
        else:
            px = player_grid[nr][nc]
            rx, cx, dx, sx, gunx = player_lst[px]  # 상대 정보
            win_idx = lose_idx = 0
            my_power = gun + s
            other_power = gunx + sx
            if my_power > other_power:
                win_idx, lose_idx = p, px
            elif my_power == other_power:
                if s > sx:
                    win_idx, lose_idx = p, px
                else:
                    win_idx, lose_idx = px, p
            else:
                win_idx, lose_idx = px, p
            score[win_idx] += abs(my_power - other_power)
            move(win_idx, lose_idx, nr, nc)

print(*score[1:])
