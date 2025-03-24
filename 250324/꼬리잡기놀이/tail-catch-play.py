'''
교수님 bfs 참조
'''

from collections import deque

n, team_num, order_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

team_lst = []
visited = [[-1] * n for i in range(n)]

numbering = 0
team_cnt = []

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(sr, sc, numbering):
    q = deque([(sr, sc)])
    cnt = 0
    while q:
        r, c = q.popleft()
        if grid[r][c] != 4:
            cnt += 1
        tmp.append([grid[r][c], (r, c)])
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] != -1 or grid[nr][nc] == 0:
                continue
            if grid[nr][nc] == 2:
                visited[nr][nc] = numbering
                q.append((nr, nc))
            elif grid[nr][nc] != 2 and (r, c) != (sr, sc):
                visited[nr][nc] = numbering
                q.append((nr, nc))
    team_cnt.append(cnt)


for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            visited[i][j] = numbering
            tmp = []
            bfs(i, j, numbering)
            numbering += 1
            team_lst.append(tmp)

ans = 0

for order in range(order_num):

    # 1. 이동
    for team in team_lst:
        team.insert(0, team.pop())
    # 1-1. 머리/몽통/꼬리 다시 표시
    for w in range(team_num):
        how = team_cnt[w]
        # 머리
        team_lst[w][0][0] = 1
        # 몸통
        for l in range(1, how - 1):
            team_lst[w][l][0] = 2
        # 꼬리
        team_lst[w][how - 1][0] = 3
        # 나머지
        for l in range(how, len(team_lst[w])):
            team_lst[w][l][0] = 4

    # 1-2. 이동한 거 토대로 맵 다시 반영
    new_grid = [[0] * n for i in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state

    # 2. 공굴려
    mok = order // n
    find = False
    team = -1
    if mok % 4 == 0:
        idx = order % n
        for j in range(n):
            if 1 <= new_grid[idx][j] <= 3:
                team = visited[idx][j]
                for w in range(len(team_lst[team])):
                    num, (r, c) = team_lst[team][w]
                    # 2-1. 점수 획득
                    if (r, c) == (idx, j):
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
            if find:
                break
    elif mok % 4 == 2:
        idx = n - order % n - 1
        for j in range(n - 1, -1, -1):
            if 1 <= new_grid[idx][j] <= 3:
                team = visited[idx][j]
                for w in range(len(team_lst[team])):
                    num, (r, c) = team_lst[team][w]
                    # 2-1. 점수 획득
                    if (r, c) == (idx, j):
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
            if find:
                break
    elif mok % 4 == 3:
        jdx = n - order % n - 1
        for i in range(n):
            if 1 <= new_grid[i][jdx] <= 3:
                team = visited[i][jdx]
                for w in range(len(team_lst[team])):
                    num, (r, c) = team_lst[team][w]
                    # 2-1. 점수 획득
                    if (r, c) == (i, jdx):
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
            if find:
                break
    elif mok % 4 == 1:
        jdx = order % n
        for i in range(n - 1, -1, -1):
            if 1 <= new_grid[i][jdx] <= 3:
                team = visited[i][jdx]
                for w in range(len(team_lst[team])):
                    num, (r, c) = team_lst[team][w]
                    # 2-1. 점수 획득
                    if (r, c) == (i, jdx):
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
            if find:
                break

    if find:
        tmp = []
        how = team_cnt[team]
        for w in range(how - 1, -1, -1):
            tmp.append(team_lst[team][w])
        for w in range(len(team_lst[team]) - 1, how - 1, -1):
            tmp.append(team_lst[team][w])
        team_lst[team] = tmp

        # 2-2. 머리/몽통/꼬리 다시 표시
        how = team_cnt[team]
        # 머리
        team_lst[team][0][0] = 1
        # 몸통
        for l in range(1, how - 1):
            team_lst[team][l][0] = 2
        # 꼬리
        team_lst[team][how - 1][0] = 3
        # 나머지
        for l in range(how, len(team_lst[team])):
            team_lst[team][l][0] = 4

    # 2-3. 변환한거 토대로 맵 반영
    new_grid = [[0] * n for i in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state

    grid = new_grid


print(ans)
