from collections import deque

n, m, bn = map(int, input().split())

grid = [list(map(int, input().split())) for i in range(n)]
cube = [[list(map(int, input().split())) for i in range(m)] for i in range(5)]
time_tmp = [list(map(int, input().split())) for i in range(bn)]
row = [0, 0, 1, -1]
col = [1, -1, 0, 0]


# 동  서  남  북


def find_three():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 3:
                return i, j


# 3차원 시작점
three_first_r, three_first_c = find_three()


def find_two_end():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 4:
                grid[i][j] = 0
                return i, j


# 2차원 탈출구
two_er, two_ec = find_two_end()


# 2차원 시작점 및 3차원 탈출구
def find_two_start_three_end():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 3:
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and (grid[nr][nc] == 0 or grid[nr][nc] == 4):
                        if k == 0:
                            return nr, nc, k, m - 1, m - 1 - (nr - three_first_r)
                        elif k == 1:
                            return nr, nc, k, m - 1, nr - three_first_r
                        elif k == 2:
                            return nr, nc, k, m - 1, nc - three_first_c
                        elif k == 3:
                            return nr, nc, k, m - 1, m - 1 - (nc - three_first_c)


two_sr, two_sc, three_eh, three_er, three_ec = find_two_start_three_end()


def find_three_start():
    for i in range(m):
        for j in range(m):
            if cube[4][i][j] == 2:
                return 4, i, j


three_sh, three_sr, three_sc = find_three_start()

time_error = [[[] for i in range(n)] for i in range(n)]
for tr, tc, td, tv in time_tmp:
    time = 0
    while True:
        time_error[tr][tc].append(time)
        ntr = tr + row[td]
        ntc = tc + col[td]
        if not (0 <= ntr < n and 0 <= ntc < n) or grid[ntr][ntc] != 0:
            break
        time += tv
        tr = ntr
        tc = ntc


def bfs3():
    visited = [[[False] * m for i in range(m)] for i in range(5)]
    visited[three_sh][three_sr][three_sc] = True
    q = deque([(three_sh, three_sr, three_sc, 0)])
    while q:
        h, r, c, cnt = q.popleft()
        if (h, r, c) == (three_eh, three_er, three_ec):
            return cnt

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            nh = h
            if nh == 4:  # 동서남북 갈 수 있음
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
                    nr = 0
                    nc = nr
                elif nc >= m:  # 동
                    nh = 0
                    nr = 0
                    nc = m - 1 - nr
            elif nh == 0:  # 동: 위남북 갈 수 있음
                if nr < 0:  # 윗면
                    nh = 4
                    nr = m - 1 - nc
                    nc = m - 1
                elif nc < 0:  # 남
                    nh = 2
                    nr = nr
                    nc = m - 1
                elif nc >= m:  # 북
                    nh = 3
                    nr = nr
                    nc = 0
            elif nh == 1:  # 서: 위북남 갈 수 있음
                if nr < 0:  # 윗면
                    nh = 4
                    nr = nc
                    nc = 0
                elif nc < 0:  # 북
                    nh = 3
                    nr = nr
                    nc = m - 1
                elif nc >= m:  # 남
                    nh = 2
                    nr = nr
                    nc = 0
            elif nh == 2:  # 남: 위서동 갈 수 있음
                if nr < 0:  # 윗면
                    nh = 4
                    nr = m - 1
                    nc = nc
                elif nc < 0:  # 서
                    nh = 1
                    nr = nr
                    nc = m - 1
                elif nc >= m:  # 동
                    nh = 0
                    nr = nr
                    nc = 0
            elif nh == 3:  # 북: 위동서 갈 수 있음
                if nr < 0:  # 윗면
                    nh = 4
                    nr = 0
                    nc = m - 1 - nr
                elif nc < 0:  # 동
                    nh = 0
                    nr = nr
                    nc = m - 1
                elif nc >= m:  # 서
                    nh = 1
                    nr = nr
                    nc = 0
            if not (0 <= nr < m and 0 <= nc < m) or visited[nh][nr][nc] or cube[nh][nr][nc]:
                continue
            visited[nh][nr][nc] = True
            q.append((nh, nr, nc, cnt + 1))
    return -1


def bfs2():
    visited = [[False] * n for i in range(n)]
    visited[two_sr][two_sc] = True
    q = deque([(two_sr, two_sc, 0)])
    while q:
        r, c, cnt = q.popleft()
        if (r, c) == (two_er, two_ec):
            return cnt

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] == 1:
                continue
            te = False
            for error in time_error[nr][nc]:
                if cnt + 1 + ans3 >= error:
                    te = True
                    break
            if not te:
                visited[nr][nc] = True
                q.append((nr, nc, cnt + 1))
    return -1


ans = -1
ans3 = bfs3()
if ans3 != -1:
    ans3 += 1
    te = False
    for error in time_error[two_sr][two_sc]:
        if ans3 >= error:
            te = True
            break
    if not te:
        ans2 = bfs2()
        if ans2 != -1:
            ans = ans3 + ans2
print(ans)
