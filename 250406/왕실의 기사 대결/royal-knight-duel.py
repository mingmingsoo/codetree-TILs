'''
문제설명
    1. 기사이동
    2. 데미지
8 5 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 1 2 1 1
2 2 2 1 1
2 3 2 1 1
2 4 2 1 1
2 5 2 1 1

8 5 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 1 2 1 1
2 2 2 1 1
2 3 2 1 1
2 4 2 1 1
2 5 2 1 1
1 1
'''
from collections import deque

n, pn, on = map(int, input().split())
grid = [[2] * (n + 2)] + [[2] + list(map(int, input().split())) + [2] for i in range(n)] + [[2] * (n + 2)]
n += 2
player_grid = [[0] * n for i in range(n)]
player_lst = [0]
for p in range(pn):
    r, c, h, w, hp = map(int, input().split())
    player_lst.append((r, c, h, w, hp, 0))
    for i in range(r, r + h):
        for j in range(c, c + w):
            player_grid[i][j] = (p + 1)
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]


def bfs(idx, nr, nc, nh, nw):
    visited = [False] * (pn + 1)
    visited[idx] = True
    q = deque([(idx, nr, nc, nh, nw)])
    tmp = []
    while q:
        idx, r, c, h, w = q.popleft()
        tmp.append(idx)
        for i in range(r, r + h):
            for j in range(c, c + w):
                if grid[i][j] == 2:
                    return []
                if player_grid[i][j] and not visited[player_grid[i][j]]:
                    visited[player_grid[i][j]] = True
                    pr, pc, ph, pw, php, pdamage = player_lst[player_grid[i][j]]
                    npr, npc = pr + row[d], pc + col[d]
                    q.append((player_grid[i][j], npr, npc, ph, pw))

    return tmp


for o in range(on):
    idx, d = map(int, input().split())
    if not player_lst[idx]:
        continue
    r, c, h, w, hp, damage = player_lst[idx]
    nr, nc = r + row[d], c + col[d]
    move_lst = bfs(idx, nr, nc, h, w)
    if not move_lst:  # 이동 불가
        continue
    for pidx in move_lst:
        r, c, h, w, hp, damage = player_lst[pidx]
        nr = r + row[d]
        nc = c + col[d]
        if pidx != idx:
            sick = 0
            for i in range(nr, nr + h):
                for j in range(nc, nc + w):
                    if grid[i][j] == 1:
                        sick += 1
            hp -= sick
            damage += sick
        if hp <= 0:
            player_lst[pidx] = 0  # 쥬금
        else:
            player_lst[pidx] = (nr, nc, h, w, hp, damage)
    player_grid = [[0] * n for i in range(n)]
    for pidx, player in enumerate(player_lst):
        if player == 0:
            continue
        r, c, h, w, hp, damage = player
        for i in range(r, r + h):
            for j in range(c, c + w):
                player_grid[i][j] = pidx


ans = 0

for pidx, player in enumerate(player_lst):
    if player == 0:
        continue
    r, c, h, w, hp, damage = player
    ans += damage
print(ans)