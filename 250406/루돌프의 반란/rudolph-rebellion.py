'''
문제설명
    1. 루돌프 이동
    2. 산타 이동
입력
    맵 n 턴 수 m 산타 수 p 루돌프 힘 c 산타 힘 d
    루돌프 위치
    산타 번호와 위치

5 1 4 1 1
5 1
1 4 2
2 3 3
3 2 4
4 1 5

5 2 4 1 1
5 1
1 5 2
2 5 3
3 5 4
4 5 5

'''
from collections import deque

n, turn, sn, rp, sp = map(int, input().split())
rr, rc = map(lambda x: int(x) - 1, input().split())
grid = [[0] * n for i in range(n)]
santa_lst = [0] * (sn + 1)
row = [-1, 0, 1, 0, 1, 1, -1, -1]
col = [0, 1, 0, -1, 1, -1, 1, -1]
change = [2, 3, 0, 1]
for s in range(sn):
    idx, r, c = map(int, input().split())
    santa_lst[idx] = [r - 1, c - 1, 0]  # 기절 시간
    grid[r - 1][c - 1] = idx
score = [0] * (sn + 1)


def cal(rr, rc, sr, sc):
    return (rr - sr) ** 2 + (rc - sc) ** 2


def jump(nr, nc, d):
    q = deque([(nr, nc)])
    tmp = []
    while q:
        qr, qc = q.popleft()
        tmp.append(grid[qr][qc])
        nqr, nqc = qr + row[d], qc + col[d]
        if 0 <= nqr < n and 0 <= nqc < n and grid[nqr][nqc]:
            q.append((nqr, nqc))
    return tmp


def merge(rr, rc, idx, d, power):
    global score
    # 점수 맥이고 기절
    santa_lst[idx][2] = t  # 기절!
    score[idx] += power
    grid[rr][rc] = 0

    # 산타 이동
    nr = rr + row[d] * power
    nc = rc + col[d] * power
    if not (0 <= nr < n and 0 <= nc < n):  # 쥬금
        santa_lst[idx] = 0
        return
    if grid[nr][nc] == 0:  # 빈 공간이면 충돌 없성
        grid[nr][nc] = idx
        santa_lst[idx][0] = nr
        santa_lst[idx][1] = nc
    else:
        # 충돌 발생....
        move_lst = jump(nr, nc, d)
        move_lst.reverse()
        for jdx in move_lst:
            # 한 칸 씩만 밀리넹..
            sr, sc, stun = santa_lst[jdx]
            nsr = sr + row[d]
            nsc = sc + col[d]
            if not (0 <= nsr < n and 0 <= nsc < n):
                santa_lst[jdx] = 0  # 쥬금
                grid[sr][sc] = 0
            else:
                santa_lst[jdx][0] = nsr
                santa_lst[jdx][1] = nsc
                grid[sr][sc], grid[nsr][nsc] = grid[nsr][nsc], grid[sr][sc]

        grid[nr][nc] = idx
        santa_lst[idx][0] = nr
        santa_lst[idx][1] = nc


def ru_move():
    global rr, rc
    lst = []
    for idx, santa in enumerate(santa_lst):
        if santa == 0:  # 쥬근애 빼고
            continue
        sr, sc, stun = santa
        dist = cal(rr, rc, sr, sc)
        lst.append((dist, -sr, -sc, idx))

    lst.sort()
    dist, sr, sc, idx = lst[0]
    sr *= -1
    sc *= -1
    lst = []
    for k in range(8):
        nr = rr + row[k]
        nc = rc + col[k]
        dist = cal(nr, nc, sr, sc)
        lst.append((dist, nr, nc, idx, k))
    lst.sort()
    dist, nr, nc, idx, d = lst[0]
    rr, rc = nr, nc  # 루돌프 위치 변환
    if grid[rr][rc]:  # 충돌 발생
        merge(rr, rc, idx, d, rp)


def santa_move():
    for idx, santa in enumerate(santa_lst):
        if santa == 0:  # 쥬근애 빼고
            continue
        sr, sc, stun = santa
        if stun and stun >= t - 1:  # 기절빼고
            continue
        cur = cal(rr, rc, sr, sc)
        lst = []
        for k in range(4):
            nr = sr + row[k]
            nc = sc + col[k]
            next = cal(rr, rc, nr, nc)
            if 0 <= nr < n and 0 <= nc < n and next < cur and grid[nr][nc] == 0:
                lst.append((next, k, nr, nc))
        if lst:
            lst.sort()
            dist, d, nr, nc = lst[0]
            santa_lst[idx][0] = nr
            santa_lst[idx][1] = nc
            grid[sr][sc], grid[nr][nc] = grid[nr][nc], grid[sr][sc]
            if (nr, nc) == (rr, rc):
                merge(rr, rc, idx, change[d], sp)
        # print(idx,"번 산타 이동 후")
        # myprint()

def myprint():
    for i in range(n):
        for j in range(n):
            if (i, j) == (rr, rc):
                print("R", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()

# myprint()
for t in range(1, turn + 1):
    # print("---",t,"---")
    # 1. 루돌프 이동
    ru_move()
    # print("루돌프 이동 후")
    # myprint()
    # 2. 산타 이동
    santa_move()
    # myprint()
    all_die = True
    for idx, santa in enumerate(santa_lst):
        if santa:
            score[idx] += 1
            all_die = False
    if all_die:
        break
    # print(santa_lst)
print(*score[1:])
