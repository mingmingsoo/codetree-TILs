'''
문제 설명
    1. 편의점 이동
    2. 편의점 도착
    3. 베켐 이동
필요한 함수
    con_go
    base_go
필요한 변수
    block
    block_tmp
    player_lst
    grid - 베이스 캠프를 나타냄
'''
from collections import deque

n, pn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
player_end = [tuple(map(lambda x: int(x) - 1, input().split())) for i in range(pn)]

player_lst = [(-1, -1) for i in range(pn)]
block = [[0] * n for i in range(n)]

time = 0

row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]


def con_go(idx, r, c):
    er, ec = player_end[idx]
    visited = [[False] * n for i in range(n)]
    visited[r][c] = True
    q = deque([(r, c, [])])
    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            return path[0][0], path[0][1]

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or block[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, path + [(nr, nc)]))


def base_go(idx):
    # 편의점에서 가까운 베켐 찾기
    base = []
    er, ec = player_end[idx]
    visited = [[False] * n for i in range(n)]
    visited[er][ec] = True
    q = deque([(er, ec)])
    while q:
        for qs in range(len(q)):
            r, c = q.popleft()
            for k in range(4):
                nr = r + row[k]
                nc = c + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or block[nr][nc]:
                    continue
                visited[nr][nc] = True
                q.append((nr, nc))
                if grid[nr][nc] == 1:
                    base.append((nr, nc))
        if base:
            base.sort()
            return base[0][0], base[0][1]


def is_end():
    for idx, location in enumerate(player_lst):
        if location != player_end[idx]:
            return False
    return True


while True:
    block_tmp = []
    # 1. 편의점 이동
    # print("==",time,"==")
    # print("before", player_lst)
    for idx, location in enumerate(player_lst):
        if location == player_end[idx]:  # 이미 도착
            continue
        if location == (-1, -1):  # 베켐도 못감
            continue
        r, c = location
        nr, nc = con_go(idx, r, c)
        player_lst[idx] = (nr, nc)
        if (nr, nc) == player_end[idx]:
            block_tmp.append((nr, nc))

    for block_r, block_c in block_tmp:
        block[block_r][block_c] = 1
    # 2. 베켐 이동
    for idx, location in enumerate(player_lst):
        if idx <= time and location == (-1, -1):
            br, bc = base_go(idx)
            player_lst[idx] = (br, bc)
            block_tmp.append((br, bc))
    for block_r, block_c in block_tmp:
        block[block_r][block_c] = 1
    # print("after", player_lst)
    time += 1
    if is_end():
        break

print(time)
