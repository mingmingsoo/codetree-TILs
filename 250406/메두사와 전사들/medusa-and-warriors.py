'''
8 4
3 3 7 7
5 2 5 5 2 6 2 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0

4 1
0 0 3 3
2 3
0 1 0 0
1 1 0 0
0 0 0 0
0 0 0 0
'''
from collections import deque

medusa_dict = {0: (7, 0, 1),
               1: (5, 4, 3),
               2: (7, 6, 5),
               3: (1, 2, 3)}
junsa_dict = {(0, -1): (7, 0), (0, 0): (0,), (0, 1): (0, 1),
              (1, -1): (5, 4), (1, 0): (4,), (1, 1): (4, 3),
              (2, -1): (7, 6), (2, 0): (6,), (2, 1): (6, 5),
              (3, -1): (1, 2), (3, 0): (2,), (3, 1): (2, 3)}

n, jn = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
tmp = list(map(int, input().split()))
junsa_lst = []
for j in range(0, jn * 2, 2):
    jr, jc = tmp[j], tmp[j + 1]
    junsa_lst.append((jr, jc))
grid = [list(map(int, input().split())) for i in range(n)]
row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]


def bfs():
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, [])])
    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            return path
        for k in (0, 4, 6, 2):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, path + [(nr, nc)]))
    return -1

def medusa_view(r, c, v):
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        for k in medusa_dict[v]:
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = 1
            q.append((nr, nc))


def junsa_view(jr, jc, v, booho):
    q = deque([(jr, jc)])
    while q:
        jr, jc = q.popleft()
        for k in junsa_dict[(v, booho)]:
            nr = jr + row[k]
            nc = jc + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or not view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = 0
            q.append((nr, nc))


def booho(c, jc):
    if c - jc > 0:
        return -1
    elif c == jc:
        return 0
    else:
        return 1

path = bfs()  # -1 이면 -1 출력
if path == -1:
    print(-1)
else:
    for r, c in path:
        if (r, c) == (er, ec):
            print(0)
            break
        total_dist, total_doll, total_attack = 0, 0, 0
        # 1. 이동한 곳에 전사 위치
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                junsa_lst.pop(i)

        # 2. 메두사의 시선
        lst = []
        for v in range(4):  # v 방향
            view_grid = [[0] * n for i in range(n)]
            medusa_view(r, c, v)
            for jr, jc in junsa_lst:
                if view_grid[jr][jc]:
                    if v in (0, 1):
                        junsa_view(jr, jc, v, booho(c, jc))
                    else:
                        junsa_view(jr, jc, v, booho(r, jr))
            doll = 0
            for jr, jc in junsa_lst:
                if view_grid[jr][jc]:
                    doll += 1
            lst.append((-doll, v, view_grid))

        lst.sort()
        doll, v, view = lst[0]
        total_doll += abs(doll)

        # 3. 전사 이동 1
        for idx, junsa in enumerate(junsa_lst):
            jr, jc = junsa
            if view[jr][jc]:
                continue
            cur = abs(jr - r) + abs(jc - c)
            for k in (0, 4, 6, 2):
                nr = jr + row[k]
                nc = jc + col[k]
                next = abs(nr - r) + abs(nc - c)
                if 0 <= nr < n and 0 <= nc < n and not view[nr][nc] and next < cur:
                    total_dist += 1
                    junsa_lst[idx] = (nr, nc)
                    break
        # 4. 전사 이동 2
        for idx, junsa in enumerate(junsa_lst):
            jr, jc = junsa
            if view[jr][jc]:
                continue
            cur = abs(jr - r) + abs(jc - c)
            for k in (6, 2, 0, 4):
                nr = jr + row[k]
                nc = jc + col[k]
                next = abs(nr - r) + abs(nc - c)
                if 0 <= nr < n and 0 <= nc < n and not view[nr][nc] and next < cur:
                    total_dist += 1
                    junsa_lst[idx] = (nr, nc)
                    break

        # 5. 이동한 곳에 메두사 위치
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                junsa_lst.pop(i)
                total_attack += 1
        print(total_dist, total_doll, total_attack)
