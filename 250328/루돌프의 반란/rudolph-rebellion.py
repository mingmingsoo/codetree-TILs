'''
코드리팩토링: 겹치는 로직 함수화
1회 틀: sr, sr 이러고 있음
2회 틀: 루돌프 충돌 수정해놓고 산타 충돌은 수정안함 미쳤어?
'''
from collections import deque

n, time, santa_num, rup, sp = map(int, input().split())
deer_r, deer_c = map(lambda x: int(x) - 1, input().split())
grid = [[0] * n for i in range(n)]
santa_lst = [0] * (santa_num + 1)
score = [0] * (santa_num + 1)
for s in range(santa_num):
    sidx, sr, sc = map(int, input().split())
    grid[sr - 1][sc - 1] = sidx
    santa_lst[sidx] = [sr - 1, sc - 1, -1]
row = [-1, 0, 1, 0, 1, 1, -1, -1]
col = [0, 1, 0, -1, 1, -1, 1, -1]
dirs = {0: 2, 1: 3, 2: 0, 3: 1}  # 반대 방향


def ru_move():
    global deer_r, deer_c
    close_santa = []
    for santa in santa_lst:
        if santa == 0:  # 죽은 애 넘어가
            continue
        i, j = santa[0], santa[1]
        close_santa.append(((i - deer_r) ** 2 + (j - deer_c) ** 2, -i, -j))

    close_santa.sort()
    dist, sr, sc = close_santa[0]
    sr *= -1
    sc *= -1

    cur = (deer_r - sr) ** 2 + (deer_c - sc) ** 2
    ori_r, ori_c = deer_r, deer_c

    for k in range(8):
        nr = ori_r + row[k]
        nc = ori_c + col[k]
        if not (0 <= nr < n and 0 <= nc < n):
            continue
        next = (nr - sr) ** 2 + abs(nc - sc) ** 2
        if next < cur:
            cur, deer_r, deer_c, d = next, nr, nc, k

    if grid[deer_r][deer_c]:  # 충돌 발생!!
        idx = grid[deer_r][deer_c]
        score[idx] += rup
        nsr = deer_r + row[d] * rup
        nsc = deer_c + col[d] * rup

        jump_santa(sr, sc, nsr, nsc, idx, d)


def merge(sr, sc, sd, move_lst):
    q = deque()
    if grid[sr][sc]:
        q.append(grid[sr][sc])

    while q:
        idx = q.popleft()
        move_lst.append(idx)
        sr, sc = santa_lst[idx][0], santa_lst[idx][1]
        nsr = sr + row[sd]
        nsc = sc + col[sd]
        if 0 <= nsr < n and 0 <= nsc < n and grid[nsr][nsc]:
            q.append(grid[nsr][nsc])


def jump_santa(sr, sc, nsr, nsc, idx, sd):
    if not (0 <= nsr < n and 0 <= nsc < n):
        santa_lst[idx] = 0  # 쥬금
        grid[sr][sc] = 0  # 쥬금
    else:
        move_lst = []
        merge(nsr, nsc, sd, move_lst)
        move_lst.sort(reverse=True)

        for jump_idx in move_lst:
            jr, jc, jsleep = santa_lst[jump_idx]
            njr = jr + row[sd]
            njc = jc + col[sd]
            if not (0 <= njr < n and 0 <= njc < n):
                santa_lst[jump_idx] = 0  # 쥬금
            else:
                grid[njr][njc] = jump_idx
                santa_lst[jump_idx][0] = njr
                santa_lst[jump_idx][1] = njc

        # 기절해!!
        santa_lst[idx][0] = nsr
        santa_lst[idx][1] = nsc
        santa_lst[idx][2] = t  # 기절!
        grid[sr][sc] = 0
        grid[nsr][nsc] = idx


def santa_move(t):
    for idx, santa in enumerate(santa_lst):
        if santa == 0:
            continue
        sr, sc, sleep = santa
        if sleep >= 0 and t - sleep <= 1:  # 기절이면 넘어가!
            continue

        cur = (sr - deer_r) ** 2 + (sc - deer_c) ** 2
        ori_sr, ori_sc = sr, sc
        for k in range(4):
            nsr = ori_sr + row[k]
            nsc = ori_sc + col[k]
            if not (0 <= nsr < n and 0 <= nsc < n) or grid[nsr][nsc]:
                continue
            next = (nsr - deer_r) ** 2 + abs(nsc - deer_c) ** 2
            if next < cur:
                cur, sr, sc, sd = next, nsr, nsc, k
        santa_lst[idx][0] = sr
        santa_lst[idx][1] = sc
        grid[ori_sr][ori_sc] = 0
        grid[sr][sc] = idx
        if (sr, sc) == (deer_r, deer_c):  # 충돌 발생!!
            score[idx] += sp
            nsr = sr + row[dirs[sd]] * sp
            nsc = sc + col[dirs[sd]] * sp

            jump_santa(sr, sc, nsr, nsc, idx, dirs[sd])


def end():
    for santa in santa_lst:
        if santa != 0:
            return False
    return True


def scoring():
    for idx, santa in enumerate(santa_lst):
        if santa != 0:
            score[idx] += 1


def myprint():
    for i in range(n):
        for j in range(n):
            if (i, j) == (deer_r, deer_c):
                print("R", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()


for t in range(time):
    ru_move()
    santa_move(t)
    if end():
        break
    scoring()
print(*score[1:])
