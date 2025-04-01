# --------------------------------- 입력 ---------------------------------
from collections import deque

srow = [-1, -1, 0, 1, 1, 1, 0, -1]
scol = [0, 1, 1, 1, 0, -1, -1, -1]

# 방향별 메두사 시야
medusa_dict = {0: (7, 0, 1), 1: (3, 4, 5), 2: (5, 6, 7), 3: (1, 2, 3)}
# 메두사 방향, 전사 위치별 시야
junsa_dict = {(0, -1): (7, 0), (0, 0): (0,), (0, 1): (0, 1),
              (1, -1): (5, 4), (1, 0): (4,), (1, 1): (4, 3),
              (2, -1): (7, 6), (2, 0): (6,), (2, 1): (6, 5),
              (3, -1): (1, 2), (3, 0): (2,), (3, 1): (2, 3)}

n, junsa_num = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
junsa_lst = []
tmp = list(map(int, input().split()))

for junsa in range(0, junsa_num * 2, 2):
    junsa_lst.append([tmp[junsa], tmp[junsa + 1]])
grid = [list(map(int, input().split())) for i in range(n)]

# 전사 이동 방향  상하좌우       좌우상하
move_row = [[-1, 1, 0, 0], [0, 0, -1, 1]]
move_col = [[0, 0, -1, 1], [-1, 1, 0, 0]]


# --------------------------------- 함수 ---------------------------------
def medusa_bfs(v, r, c): # 메두사 시야 bfs
    # v 가 방향
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        for k in medusa_dict[v]:
            nr = r + srow[k]
            nc = c + scol[k]
            if not (0 <= nr < n and 0 <= nc < n) or view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = True # 볼 수 있어
            q.append((nr, nc))


def junsa_view(jr, jc, v, d): # 전사 시야 bfs
    q = deque([(jr, jc)])
    while q:
        r, c = q.popleft()
        for k in junsa_dict[(v, d)]:
            nr = r + srow[k]
            nc = c + scol[k]
            if not (0 <= nr < n and 0 <= nc < n) or not view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = False # 아니 볼 수 없어
            q.append((nr, nc))

def booho(nx,x): # 부호를 반환
    if nx < x : return -1
    elif nx == x : return 0
    elif nx > x : return 1

def junsa_bfs(v, r, c):
    for jr, jc in junsa_lst:
        if view_grid[jr][jc]:
            if v in (0,1):
                junsa_view(jr, jc, v, booho(jc,c))
            elif v in (2,3):
                junsa_view(jr, jc, v, booho(jr,r))


def bfs(sr, sc, er, ec): # 메두사 경로 bfs
    bfs_row = [-1, 1, 0, 0]
    bfs_col = [0, 0, -1, 1]
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, [])])
    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            return path
        for k in range(4):
            nr = r + bfs_row[k]
            nc = c + bfs_col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, path + [(nr, nc)]))

    return -1

path = bfs(sr, sc, er, ec)
if path == -1: # 공원 못가
    print(-1)
else:

    for r, c in path:
        # 메두사 위치가 지금 r,c
        if (r,c) == (er,ec):
            print(0)
            break
        move_dist, stone, attack = 0, 0, 0

        # 죽는 애 검사
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                junsa_lst.pop(i)  # 메두사가 죽임

        # 메두사 시야
        view_lst = []  # 돌이 된 전사 수 , 방향, 2차원 배열 맵
        for v in range(4):
            view_grid = [[False] * n for i in range(n)]
            medusa_bfs(v, r, c)
            junsa_bfs(v, r, c)

            # 여기서 갯수세서 넣어주자
            doll_cnt = 0
            for jr, jc in junsa_lst:
                if view_grid[jr][jc]:
                    doll_cnt += 1

            view_lst.append((-doll_cnt, v, view_grid)) # 깊은복사 안해줘도 된다.

        view_lst.sort()
        doll, d, view = view_lst.pop(0)
        stone += abs(doll)


        # 전사들 이동
        for idx, junsa in enumerate(junsa_lst):
            if view[junsa[0]][junsa[1]]:  # 돌이여유
                continue
            # 총 두번의 이동
            for turn in range(2):
                jr, jc = junsa_lst[idx]
                cur = abs(jr - r) + abs(jc - c)
                for k in range(4):
                    nr = jr + move_row[turn][k]
                    nc = jc + move_col[turn][k]
                    next = abs(nr - r) + abs(nc - c)
                    if (0 <= nr < n and 0 <= nc < n) and next < cur and not view[nr][nc]:
                        # 움직일 수 있다!
                        move_dist += 1
                        junsa_lst[idx][0] = nr
                        junsa_lst[idx][1] = nc
                        break

        # 전사 공격
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                attack += 1
                junsa_lst.pop(i) # 전사 주금
        print(move_dist, stone, attack)
