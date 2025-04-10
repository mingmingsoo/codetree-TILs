from collections import deque

n, turn, sn, rp, sp = map(int, input().split())
r, c = map(lambda x: int(x) - 1, input().split())  # 루돌푸 위치
grid = [[0] * n for i in range(n)]
santa_lst = [0] * (sn + 1)
score = [0] * (sn + 1)
for _ in range(sn):
    idx, sr, sc = map(int, input().split())
    grid[sr - 1][sc - 1] = idx
    santa_lst[idx] = [sr - 1, sc - 1, 0]  # 위치, 기절
row = [-1, 0, 1, 0, 1, 1, -1, -1]
col = [0, 1, 0, -1, 1, -1, 1, -1]
change = [2, 3, 0, 1]


def is_end():
    for idx, santa in enumerate(santa_lst):
        if santa:
            return False
    return True


def cal(x, y, nx, ny):
    return (nx - x) ** 2 + (ny - y) ** 2


def jump(nr, nc, d):
    tmp = []
    q = deque([(nr, nc)])
    while q:
        sr, sc = q.popleft()
        tmp.append(grid[sr][sc])
        nsr = sr + row[d]
        nsc = sc + col[d]
        if 0 <= nsr < n and 0 <= nsc < n and grid[nsr][nsc]:
            q.append((nsr, nsc))

    return tmp


def merge(r, c, d, power, idx):  # 루돌프 위치는 바뀌면 안됨.
    # 일단 기절 맥이고 점수 매경
    score[idx] += power
    grid[r][c] = 0
    nr = r + row[d] * power
    nc = c + col[d] * power
    if not (0 <= nr < n and 0 <= nc < n):
        santa_lst[idx] = 0
    else:
        if not grid[nr][nc]:
            grid[nr][nc] = idx
            santa_lst[idx] = [nr, nc, t]
        else:
            jump_lst = jump(nr, nc, d)
            if jump_lst:
                jump_lst.reverse()
                for jdx in jump_lst:
                    jr, jc = santa_lst[jdx][0], santa_lst[jdx][1]
                    njr = jr + row[d]
                    njc = jc + col[d]
                    if 0 <= njr < n and 0 <= njc < n:
                        grid[njr][njc], grid[jr][jc] = grid[jr][jc], grid[njr][njc]
                        santa_lst[jdx][0] = njr
                        santa_lst[jdx][1] = njc
                    else:
                        santa_lst[jdx] = 0
                        grid[jr][jc] = 0
            grid[nr][nc] = idx
            santa_lst[idx] = [nr, nc, t]


def myprint():
    for i in range(n):
        for j in range(n):
            if (i,j) == (r,c):
                print("R", end=  " ")
            elif grid[i][j]:
                print(grid[i][j], end = " ")
            else:
                print(0, end = " ")
        print()

for t in range(1, turn + 1):
    # print("-------",t,"-------")
    # 1. 루돌프 이동
    lst = []
    for idx, santa in enumerate(santa_lst):
        if not santa:
            continue
        sr, sc, stun = santa
        dist = cal(r, c, sr, sc)
        lst.append((dist, (-sr, -sc), idx))
    lst.sort()
    _, location, sidx = lst[0]
    sr, sc = -location[0], -location[1]
    # 타겟은 정해졌고 타겟과 가장 가깝게
    lst = []
    for k in range(8):
        nr = r + row[k]
        nc = c + col[k]
        if 0 <= nr < n and 0 <= nc < n:
            dist = cal(nr, nc, sr, sc)
            lst.append((dist, (nr, nc), k))
    lst.sort()
    _, location, ru_d = lst[0]
    r, c = location  # 옮겻!!

    if grid[r][c]:
        merge(r, c, ru_d, rp, grid[r][c])
    # print("루돌프 이동 후")
    # myprint()
    # 2. 산타 이동
    for idx, santa in enumerate(santa_lst):
        if not santa:
            continue
        sr, sc, stun = santa
        if stun and stun >= t - 1:  # 기절한 애들
            continue
        lst = []
        cur = cal(sr,sc,r,c)
        for k in range(4):
            nr = sr + row[k]
            nc = sc + col[k]
            if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc]:
                dist = cal(nr, nc, r, c)
                if cur > dist:
                    lst.append((dist, k, (nr, nc)))
        if lst:
            lst.sort()
            _, s_d, location = lst[0]
            nr, nc = location
            if (nr, nc) == (r, c):
                grid[sr][sc] = 0
                merge(r, c, change[s_d], sp, idx)
            else:
                # 그냥 이동
                santa_lst[idx] = [nr, nc, stun]
                grid[nr][nc], grid[sr][sc] = grid[sr][sc], grid[nr][nc]
        # print(idx,"번 산타 이동")
        # myprint()
    # 3. 살아있는 애들 +1 점
    all_die = True
    for idx, santa in enumerate(santa_lst):
        if santa:
            score[idx] += 1
            all_die = False
    if all_die:
        break
print(*score[1:])