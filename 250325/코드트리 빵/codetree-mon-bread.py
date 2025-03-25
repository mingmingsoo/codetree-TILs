'''
2. 격자에 있는~ 유의합니다. 이해 안됨
문제 설명
    m명의 사람이 정확히 m분에 각자의 베이스 캠프에서 출발해 편의점으로 이동 시작
    사람들은 출발시간이 되기 전까지 격자 밖에 있고, 모두 다른 편의점을 목표로 함
    1분 동안 진행되는 행동
    1. 격자에 있는 사람들은 가려는 편의점을 향해 1칸씩 움직임
        우선순위 ^ < > v
    2. 편의점에 도착하면 그 편의점이 벽이됨 -> 이래서 bfs가 필요할 듯
    3. 현재 시간이 t분이고 t<=m 을 만족하면 t번 사람은 편의점 가까이에 있는 베이스캠프에 들어감
        여러가지면 행이 작고 열이 작은
        베이스캠프에 사람 있으면 그 칸 못지나감
헷갈리는 거
    베켐에서 나오면 지나갈 수 있는지? -> 아닌 듯 그냥 벽처리
사람들은 겹쳐도 된다.
구상
    1. 격자밖인지 검사
        -> 격자밖이 아니면 bfs 돌려서 이동
    2. 편의점이면 편의점 벽처리
    3. 베켐갈 수 있으면 베켐가 -> 이것도 bfs 필요!!
    4. 플레이어 == 편의점이면 break

15 30
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 1
3 2
3 3
3 4
3 5
3 6
3 7
3 8
3 9
3 10
3 11
3 12
3 13
3 14
3 15
4 1
4 2
4 3
4 4
4 5
4 6
4 7
4 8
4 9
4 10
4 11
4 12
4 13
4 14
4 15


아 바로 block 하면 안되고
격자에 있는 모든 사람들이 이동 한 뒤에임!!!!!!!!!

'''
from collections import deque

n, player_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
block = [[0] * n for i in range(n)]

player_lst = []
for p in range(player_num):
    player_lst.append((-1, -1))

player_end = []  # 목적지
for p in range(player_num):
    r, c = map(int, input().split())
    player_end.append((r - 1, c - 1))


time = 0

row = [-1, 0, 0, 1]  # 이렇게 해도 우선순위가 되나?ㅜㅜ
col = [0, -1, 1, 0]


def base_go(idx):
    cr, cc = player_end[idx]  # 편의점 위치
    # 편의점 위치에서 베켐중 가까운 거리를 찾는다.
    possible = []
    q = deque([(cr, cc, 0)])
    visited = [[False] * n for i in range(n)]
    visited[cr][cc] = True

    while q:
        q_size = len(q)
        for qs in range(q_size):
            r, c, dist = q.popleft()
            if grid[r][c] == 1:
                possible.append((dist, r, c))
            for k in range(4):
                nr = r + row[k]
                nc = c + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or block[nr][nc]:
                    continue
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
        if possible:
            possible.sort()
            dist, r, c = possible[0]
            return r, c


def con_go(idx):
    r, c = player_lst[idx]  # 현재 플레이어 위치
    er, ec = player_end[idx]  # 편의점 위치
    q = deque([(r, c, 0, [])])  # 위치 거리, 경로
    visited = [[False] * n for i in range(n)]
    visited[r][c] = True
    possible = []
    while q:
        r, c, dist, path = q.popleft()
        if (r, c) == (er, ec):
            possible = path
            break
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or block[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, dist + 1, path[:] + [(nr, nc)]))
    return possible[0][0], possible[0][1]

while True:
    block_lst = []
    for idx, player in enumerate(player_lst):

        # 0. 이미 도착한 애들은 거너뛰어!
        if player == player_end[idx]:
            continue

        # 1. 가까운 편의점으로 이동
        if player != (-1, -1):
            nr, nc = con_go(idx)
            player_lst[idx] = (nr, nc)

        # 2. 편의점 도착했으면 벽처리
        er, ec = player_end[idx]
        if player_lst[idx] == (er, ec):
            block_lst.append((er,ec))

        # 3. 베켐 갈 수 있으면 베켐 가
        if time >= idx:
            if player == (-1, -1):
                for r, c in block_lst:
                    block[r][c] = 1
                base_r, base_c = base_go(idx)
                player_lst[idx] = (base_r, base_c)
                block_lst.append((base_r, base_c))
        else:
            break
    for r, c in block_lst:
        block[r][c] = 1
    time += 1
    if player_lst == player_end:
        break
print(time)