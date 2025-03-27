'''
별거 안고쳤는데 왜 맞고 틀인지 잘 모르겠음

for pid in range(len(player_lst) - 1, -1, -1):
        if pid == origin_p_id:
            continue
        if pid not in move_lst:
            continue
위에 거에서

move_lst.sort(reverse=True)
for pid in move_lst:
    if pid == origin_p_id: # 공격한애는 데미지 안먹는다!
        continue

알아냈다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


for pid in range(len(player_lst) - 1, -1, -1):

player_lst 는 딕셔너린데 예를들어 길이가 10이여도
기사 넘버가 28인 애가 들어있을 수 있음!!
그래서 움직일때 기사 넘버가 28인 애들은 pid 에 해당이 안돼서 그런겅임!!!!
유레카 유레카!!
key를 pop 해주기 때문에 reverse 도 안해줘도됨!!

'''
from collections import deque

n, player_num, order_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
n += 2
for _ in grid:
    _.append(2)
    _.insert(0, 2)

grid.insert(0, [2] * n)
grid.append([2] * n)


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


def move():  # 이동 가능한지만 본다.
    global move_possible
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
                # if not (0 <= i < n and 0 <= j < n): # 진짜 없어도 되나?
                #     continue  # break 여도 됨
                if player_grid[i][j] != -1:  # 다른 애도 이동 시켜줘야함..
                    if not visited[player_grid[i][j]]:
                        q.append((player_grid[i][j], player_lst[player_grid[i][j]]))
                        visited[player_grid[i][j]] = True
                if grid[i][j] == 2:  # 벽이면 안돼!!!!
                    move_possible = False
                    break
            if not move_possible:
                break
        if not move_possible:
            break


def minus_hp(origin_p_id):
    global player_grid
    # 일단 이동부터 시켜주고요..
    for pid in move_lst:
        player_lst[pid][0] += row[d]
        player_lst[pid][1] += col[d]
        player_lst[pid][2] += row[d]
        player_lst[pid][3] += col[d]
    # 그 다음에 데미지 처리 해줄게용 -> 뒤에서부터 해줘야되네 ㅠㅠ
    # reverse 안해줘도 된다.
    for pid in move_lst:
        if pid == origin_p_id: # 공격한애는 데미지 안먹는다!
            continue
        player = player_lst[pid]
        r, c, x, y, power, damage = player
        sick = 0
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


for p_id, d in order_lst:
    if (p_id -1) not in player_lst:  # 체스판에 없어요..
        continue
    move_lst = []
    move_possible = True
    move()
    if move_possible:
        minus_hp(p_id - 1)

ans = 0
for pid, player in player_lst.items():
    ans += player[5]
print(ans)
