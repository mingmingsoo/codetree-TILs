'''
코드 리팩토륑~ 오류 찾아서 신난다~
'''
# -------------------------- 입력 --------------------------
from collections import deque

n, player_num, order_num = map(int, input().split())
grid = [[2]*(n+2)] + [[2] + list(map(int, input().split())) + [2] for i in range(n)] + [[2]*(n+2)]
n += 2

player_lst = {}
player_grid = [[-1] * n for i in range(n)]  # 나중에 꼭 -1로 바꾸기!!!!!!!!!!!!!!!!!
for p in range(player_num):
    r, c, x, y, power = map(int, input().split())
    player_lst[p] = [r, c, r + x, c + y, power, 0]  # 받은 데미지의합
    for i in range(r, r + x):
        for j in range(c, c + y):
            player_grid[i][j] = p

order_lst = []
for i in range(order_num):
    idx, d = map(int, input().split())
    order_lst.append((idx, d))

row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]


# -------------------------- 함수 --------------------------
def move():  # 이동 가능한지만 본다.
    q = deque([(p_id - 1, player_lst[p_id - 1])])
    visited = [False] * player_num
    visited[p_id - 1] = True
    while q:
        pid, player = q.popleft()
        r, c, x, y, power, damage = player
        move_lst.append(pid)
        nr = r + row[d]
        nc = c + col[d]
        nx = x + row[d]
        ny = y + col[d]
        for i in range(nr, nx):
            for j in range(nc, ny):
                if player_grid[i][j] != -1:  # 다른 애도 이동 시켜줘야함..
                    if not visited[player_grid[i][j]]:
                        q.append((player_grid[i][j], player_lst[player_grid[i][j]]))
                        visited[player_grid[i][j]] = True
                if grid[i][j] == 2:  # 벽이면 안돼!!!!
                    return False
    return True


def minus_hp(origin_p_id):
    global player_grid
    # 일단 전부 이동부터 시켜주고요..
    for pid in move_lst:
        player_lst[pid][0] += row[d]
        player_lst[pid][1] += col[d]
        player_lst[pid][2] += row[d]
        player_lst[pid][3] += col[d]

    for pid in move_lst:
        # 공격한애는 데미지 안먹는다!
        if pid == origin_p_id:
            continue
        player = player_lst[pid]
        r, c, x, y, power, damage = player
        sick = 0 # 아야
        for i in range(r, x):
            for j in range(c, y):
                if grid[i][j] == 1:  # 데미지 감소!
                    sick += 1
        power -= sick
        damage += sick
        if power <= 0:
            player_lst.pop(pid)
        else:
            player_lst[pid][4] = power
            player_lst[pid][5] = damage

    # 그 다음에 맵에 반영!
    new_player_grid = [[-1] * n for i in range(n)]
    for pid, player in player_lst.items():
        r, c, x, y, power, damage = player
        for i in range(r, x):
            for j in range(c, y):
                new_player_grid[i][j] = pid

    player_grid = new_player_grid


# -------------------------- 메인 --------------------------
for p_id, d in order_lst:
    if (p_id - 1) not in player_lst:  # 체스판에 없어요..
        continue
    move_lst = []
    if move():
        minus_hp(p_id - 1)

ans = 0
for pid, player in player_lst.items():
    ans += player[5]
print(ans)
