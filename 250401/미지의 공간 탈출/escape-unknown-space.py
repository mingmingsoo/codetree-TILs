'''
코드 리팩토링
3차원 bfs 디버깅용 path 변수 제거
시간이상현상 2차원으로 변경
'''
# --------------------------------- 입력, 좌표찾기 ---------------------------------

from collections import deque

n, m, time_attack_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
cube = []
for _ in range(5):
    tmp = [list(map(int, input().split())) for i in range(m)]
    cube.append(tmp)

row = [0, 0, 1, -1]
col = [1, -1, 0, 0]

sh3, sr3, sc3 = -1, -1, -1  # 3차원 시작점
eh3, er3, ec3 = -1, -1, -1  # 3차원 탈출구
sr2, sc2 = -1, -1,  # 2차원 시작점
er2, ec2 = -1, -1  # 2차원 탈출구


def find():  # 3 시작 위치 찾기
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 3:
                return i, j


startx, starty = find()

for i in range(n):  # 2차원 목적지 찾기
    for j in range(n):
        if grid[i][j] == 4:
            er2, ec2 = i, j

for h in range(5):  # 3차원 시작점 찾기
    for i in range(m):
        for j in range(m):
            if cube[h][i][j] == 2:
                sh3, sr3, sc3 = h, i, j

for i in range(n):  # 2차원 시작점, 3차원 목적지 찾기
    for j in range(n):
        if grid[i][j] == 3:
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    sr2, sc2 = nr, nc  # 2차원 시작점
                    # 이제 3차원 목적지 찾기
                    eh3 = k  # k가 면 idx가 될거임.
                    er3 = m - 1  # r은 무조건 2임.
                    if k == 0:  # 동
                        ec3 = m - 1 - (nr - startx)
                    elif k == 1:  # 서
                        ec3 = nr - startx
                    elif k == 2:  # 남
                        ec3 = nc - starty
                    elif k == 3:  # 북.
                        ec3 = m - 1 - (nc - starty)
                    break

# ---------------------- 시간 이상 2차원 배열 만들기 ----------------------
time_attack = [[1000 * 20 + 1] * n for i in range(n)]
time_info = [list(map(int, input().split())) for i in range(time_attack_num)]
for tr, tc, td, tv in time_info:
    v = tv
    time_attack[tr][tc] = 0

    for k in range(n):
        ntr = tr + row[td]
        ntc = tc + col[td]
        if not (0 <= ntr < n and 0 <= ntc < n) or grid[ntr][ntc]:
            break
        time_attack[ntr][ntc] = min(tv, time_attack[ntr][ntc])
        tv += v
        tr = ntr
        tc = ntc


# --------------------------------- 함수 ---------------------------------
def bfs3(sh, sr, sc, eh, er, ec):
    visited = [[[False] * n for i in range(n)] for i in range(5)]
    visited[sh][sr][sc] = True
    q = deque([(sh, sr, sc, 0)])

    while q:
        h, r, c, time = q.popleft()
        if (h, r, c) == (eh, er, ec):
            return time

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            nh = h
            # 실수하면 큰일난다.
            if h == 4:  # 윗면이면 어디로든지 갈 수 있음
                if nr < 0:  # 북
                    nh = 3
                    nr = 0
                    nc = m - 1 - nc
                elif nr >= m:  # 남
                    nh = 2
                    nr = 0
                    nc = nc
                elif nc < 0:  # 서
                    nh = 1
                    nc = nr
                    nr = 0
                elif nc >= m:  # 동
                    nh = 0
                    nc = m - 1 - nr
                    nr = 0
            elif h == 0:  # 동쪽면은 위,북,남 갈 수 있음
                if nr < 0:  # 위로
                    nh = 4
                    nr = m - 1 - nc
                    nc = m - 1
                elif nc >= m:  # 북쪽으로
                    nh = 3
                    nc = 0
                    nr = nr
                elif nc < 0:  # 남쪽으로
                    nh = 2
                    nc = m - 1
                    nr = nr
            elif h == 1:  # 서쪽면은 위,북,남 갈 수 있음
                if nr < 0:  # 위로
                    nh = 4
                    nr = m - 1 - nc
                    nc = 0
                elif nc >= m:  # 남쪽으로
                    nh = 2
                    nc = 0
                    nr = nr
                elif nc < 0:  # 북쪽으로
                    nh = 3
                    nc = m - 1
                    nr = nr
            elif h == 2:  # 남쪽면은 위,서,동 갈 수 있음
                if nr < 0:  # 위로
                    nh = 4
                    nr = m - 1
                    nc = nc
                elif nc < 0:  # 서쪽으로
                    nh = 1
                    nc = m - 1
                    nr = nr
                elif nc >= m:  # 동쪽으로
                    nh = 0
                    nc = 0
                    nr = nr

            elif h == 3:  # 북쪽면은 위,동,서 갈 수 있음
                if nr < 0:  # 위로
                    nh = 4
                    nr = 0
                    nc = m - 1 - nc
                elif nc < 0:  # 동쪽으로
                    nh = 0
                    nc = m - 1
                    nr = nr
                elif nc >= m:  # 서쪽으로
                    nh = 1
                    nc = 0
                    nr = nr

            if not (0 <= nr < m and 0 <= nc < m) or visited[nh][nr][nc] or cube[nh][nr][nc] == 1:
                continue
            visited[nh][nr][nc] = True
            q.append((nh, nr, nc, time + 1))
    return -1


def bfs2(sr, sc, er, ec):
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, 0)])

    while q:
        r, c, time = q.popleft()
        if (r, c) == (er, ec):
            return time

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] == 1 or grid[nr][nc] == 3:
                continue
            if ans + time + 1 >= time_attack[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, time + 1))
    return -1


# --------------------------------- 메인 ---------------------------------
ans = bfs3(sh3, sr3, sc3, eh3, er3, ec3)
if ans != -1:  # ans == -1이면 3차원 탈출도 못함
    ans += 1

    if time_attack[sr2][sc2] <= ans:
        ans = -1 # 내려왔는데 시간이상..


    if ans != -1:
        next_ans = bfs2(sr2, sc2, er2, ec2)
        if next_ans == -1:  # 2차원 탈출 못함
            ans = -1
        else:
            ans += next_ans
print(ans)
