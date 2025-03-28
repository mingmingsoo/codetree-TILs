'''
문제 설명
    1. 루돌프 이동 - 8방 우선순위 거리(^2) 주의, r 큰거 , c 큰거
    2. 산타 순차 이동 - 4방 우선순위 상우하좌
구상
    상호작용이 좀 어려운데
    기사단처럼 q로 써서 움직여야 하는애들 move_lst에 담고
    옮겨주면서 격자 밖인 애들은 없애줌 걍
    아 근데 산타이동 할때 순차라
    산타 1차원 리스트로 관리해주자.

입력
맵 크기 N, 턴 수 time, 산타 수 santa_num, 루돌푸 힘 ru_p,  산타 힘 s_p
루돌푸 위치
산타 위치

필요한 변수
    - 루돌프 좌표 r,c,d 맵에 따로 표시 안한다
    - 산타 맵 2차원 배열 grid 넘버링만 해준다
        산타 1차원 배열
        방향, 기절시간 담아준다
        방향과 기절시간 초기값은 -1
        근데 죽은애는 0으로 해주자.
    - score 산타 수 + 1만큼 0번쨰에 빈 0 넣어주기
필요한 함수
    ru_move() : 루돌프 이동
        if merge() : 충돌 낫냐?
            # 여기서 기절시간 기록
            santa_jump() : 났으면 와라락 이동
    santa_move() : 산타 순차 이동
        if 기절시간 <= time -1 : continue 요롷게  해서 넘어가.
        if merge() : 충돌 낫냐?
            # 여기서 기절시간 기록
            santa_jump() : 났으면 와라락 이동
    exit() : 전부 죽었나 검사
    scoring(): 살아있는 애들 점수 추가
'''
from collections import deque

# 맵 크기 N, 턴 수 time, 산타 수 santa_num, 루돌푸 힘 ru_p,  산타 힘 s_p
# 루돌푸 위치
# 산타 위치
# 문제에서 거리는 모두 제곱인거야????

n, time, santa_num, rup, sp = map(int, input().split())
r, c = map(lambda x: int(x) - 1, input().split())
grid = [[0] * n for i in range(n)]
santa_lst = [0] * (santa_num + 1)
score = [0] * (santa_num + 1)
for s in range(santa_num):
    sidx, sr, sc = map(int, input().split())
    sr -= 1
    sc -= 1
    grid[sr][sc] = sidx
    santa_lst[sidx] = [sr,sc,-1,-1]
d = -1
# print(santa_lst)
# for _ in grid:
#     print(_)
row = [-1, 0, 1, 0, 1, 1, -1, -1]
col = [0, 1, 0, -1, 1, -1, 1, -1]

dirs = {0: 2, 1: 3, 2: 0, 3: 1}


def ru_move():
    global r, c, d
    close_santa = []
    for santa in santa_lst:
        if santa == 0:
            continue
        i, j = santa[0], santa[1]
        close_santa.append(((i - r) ** 2 + (j - c) ** 2, -i, -j))

    close_santa.sort()
    dist, sr, sc = close_santa[0]
    sr *= -1
    sc *= -1

    cur = (r - sr) ** 2 + (c - sc) ** 2
    ori_r, ori_c = r, c
    for k in range(8):
        nr = ori_r + row[k]
        nc = ori_c + col[k]
        if not (0 <= nr < n and 0 <= nc < n):
            continue
        next = (nr - sr) ** 2 + abs(nc - sc) ** 2
        if next < cur:
            cur = next
            r = nr
            c = nc
            d = k

    if grid[r][c]:  # 충돌 발생!!
        idx = grid[r][c]
        score[idx] += rup
        nsr = r + row[d] * rup
        nsc = c + col[d] * rup
        if not (0 <= nsr < n and 0 <= nsc < n):
            santa_lst[idx] = 0  # 쥬금
            grid[sr][sc] = 0  # 쥬금
        else:
            move_lst = []
            merge(nsr, nsc, d, move_lst)
            move_lst.sort(reverse=True)
            # print("연쇄 이동할 애들:", move_lst)
            for jump_idx in move_lst:
                jr, jc, jd, jsleep = santa_lst[jump_idx]
                njr = jr + row[d]
                njc = jc + col[d]
                if not (0 <= njr < n and 0 <= njc < n):
                    santa_lst[jump_idx] = 0  # 쥬금
                else:
                    grid[jr][jc] = 0
                    grid[njr][njc] = jump_idx
                    santa_lst[jump_idx][0] = njr
                    santa_lst[jump_idx][1] = njc
                    santa_lst[jump_idx][2] = d

            # 기절해!!
            santa_lst[idx][0] = nsr
            santa_lst[idx][1] = nsc
            santa_lst[idx][2] = d
            grid[r][c] = 0
            grid[nsr][nsc] = idx
            santa_lst[idx][3] = t  # 기절!


def merge(sr, sc, sd, move_lst):
    q = deque()
    if grid[sr][sc]:
        q.append(grid[sr][sc])

    while q:
        idx = q.popleft()
        move_lst.append(idx)
        sr, sc = santa_lst[idx][0], santa_lst[idx][0]
        nsr = sr + row[sd]
        nsc = sc + col[sd]
        if 0 <= nsr < n and 0 <= nsc < n and grid[nsr][nsc]:
            q.append(grid[nsr][nsc])


def santa_move(t):
    for idx, santa in enumerate(santa_lst):
        if santa == 0:
            continue
        sr, sc, sd, sleep = santa
        if sleep >= 0 and t - sleep <= 1:  # 기절이면 넘어가!
            continue

        cur = (sr - r) ** 2 + (sc - c) ** 2
        ori_sr, ori_sc = sr, sc
        for k in range(4):
            nsr = ori_sr + row[k]
            nsc = ori_sc + col[k]
            if not (0 <= nsr < n and 0 <= nsc < n) or grid[nsr][nsc]:
                continue
            next = (nsr - r) ** 2 + abs(nsc - c) ** 2
            if next < cur:
                cur = next
                sr = nsr
                sc = nsc
                sd = k
        santa_lst[idx][0] = sr
        santa_lst[idx][1] = sc
        santa_lst[idx][2] = sd
        grid[ori_sr][ori_sc] = 0
        grid[sr][sc] = idx
        if (sr, sc) == (r, c):  # 충돌 발생!!
            score[idx] += sp
            nsr = sr + row[dirs[sd]] * sp
            nsc = sc + col[dirs[sd]] * sp
            if not (0 <= nsr < n and 0 <= nsc < n):
                santa_lst[idx] = 0  # 쥬금
                grid[sr][sc] = 0  # 쥬금
            else:
                move_lst = []
                merge(nsr, nsc, dirs[sd], move_lst)
                move_lst.sort(reverse=True)
                # print("연쇄 이동할 애들:", move_lst)
                for jump_idx in move_lst:
                    jr, jc, jd, jsleep = santa_lst[jump_idx]
                    njr = jr + row[dirs[sd]]
                    njc = jc + col[dirs[sd]]
                    if not (0 <= njr < n and 0 <= njc < n):
                        santa_lst[jump_idx] = 0  # 쥬금
                    grid[jr][jc] = 0
                    grid[njr][njc] = jump_idx
                    santa_lst[jump_idx][0] = njr
                    santa_lst[jump_idx][1] = njc
                    santa_lst[jump_idx][2] = dirs[sd]

                # 기절해!!
                santa_lst[idx][0] = nsr
                santa_lst[idx][1] = nsc
                santa_lst[idx][2] = dirs[sd]
                grid[sr][sc] = 0
                grid[nsr][nsc] = idx
                santa_lst[idx][3] = t  # 기절!


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
            if (i, j) == (r, c):
                print("R", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()


for t in range(time):
    #   ru_move() : 루돌프 이동
    # print("루돌푸 이동 전: ", (r, c))
    ru_move()
    # print("루돌푸 이동 후: ", (r, c))
    # myprint()
    # santa_move() : 산타 순차 이동
    santa_move(t)
    # print("-----산타 이동 후------")
    # myprint()
    #     exit() : 전부 죽었나 검사
    if end():
        break
    #     scoring(): 살아있는 애들 점수 추가
    scoring()
print(*score[1:])
