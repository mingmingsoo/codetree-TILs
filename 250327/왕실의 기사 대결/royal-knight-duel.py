'''
어렵다.
문제 설명
    1. 기사 이동
        - d 방향으로 한 칸 이동
        - 다른 기사가 있으면 연쇄적으로 이동
        - 벽 있으면 불가
        - 격자 밖으로 쫓겨날 수도 있음
        - 체스판에서 사라진 기사도  호출 될 수 있음, 반응은 X
    2. 대결
        - 이동한 곳에 함정 수 만큼 대미지 먹음
        - 0되면 사라짐
        - 민 기사도 일단 이동 후에 대미지 받음 얘도 0되면 사라짐
구상
    1번이 어려운데 q를 써서 해보자.
    벽 만나면 False 줘서 이동 안하게 하겠다
    그리고 가면서 이동시켜야 하는 애들의 넘버를 [] 기록해두고
    걔네를 한번에 이동 시킨다.
    이동 시키고 나서 r,c 가 범위 벗어나면  remove 해준다 나간거니까

입력
    맵 크기 l, 기사수 n, 명령수 q
    맵 정보
    기사 정보
    명령 정보
출력
    생존한 기사들이 받은 대미지의 합? wow
필요한 변수
    player_lst = [(sr,sc,er,ec,power), ...]
    player_map 2차원 배열 -1로 초기화하고 넘버만 표시
    grid 2차원 배열 벽과 함정만
필요한 함수
    move() - 여기서 근데 좀 어려울 듯 이동 가능한지를 일단 알아놔야됨
    minus_hp() - 이동시킨거 기반 피깎기

궁굼한게 기사 이동시켰는데 지혼자 격자밖으로 나가는 경우도 있음? 아니면 한칸만이나??
아 체스밖도 벽으로 간주...?


4 3 4
0 0 1 0
0 0 1 0
1 1 0 1
0 0 2 0
1 2 2 1 5
2 1 2 1 1
3 2 1 2 3
1 2
2 1
3 3
2 0

사라진 기사 호출


4 3 1
0 0 0 0
0 0 0 0
0 0 0 0
2 2 2 2
1 1 1 2 5
2 1 1 2 5
3 1 1 2 5
1 2

안밀려요
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


def minus_hp(origin_p_id):
    global player_grid
    # 일단 이동부터 시켜주고요..
    for pid in move_lst:
        player_lst[pid][0] += row[d]
        player_lst[pid][1] += col[d]
        player_lst[pid][2] += row[d]
        player_lst[pid][3] += col[d]

    # 그 다음에 데미지 처리 해줄게용 -> 뒤에서부터 해줘야되네 ㅠㅠ
    for pid in range(len(player_lst) - 1, -1, -1):
        if pid == origin_p_id:
            continue
        if pid not in move_lst:
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
