'''
함수화
'''
from collections import deque


def bfs(sr, sc, team_numbering):
    q = deque([(sr, sc)])
    tr, tc = -1, -1  # 꼬리 기록
    cnt = 0
    while q:
        r, c = q.popleft()
        cnt += 1
        tmp.append([grid[r][c], (r, c)])
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if 1 <= grid[nr][nc] <= 2 and not visited[nr][nc]:
                visited[nr][nc] = team_numbering
                q.append((nr, nc))
            if grid[nr][nc] == 3:
                tr, tc = nr, nc
    team_info.append(cnt + 1)
    return tr, tc


def bfs4(tr, tc, team_numbering):
    q = deque([(tr, tc)])
    while q:
        r, c = q.popleft()
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if grid[nr][nc] == 4 and not visited[nr][nc]:
                visited[nr][nc] = team_numbering
                tmp.append([grid[nr][nc], (nr, nc)])
                q.append((nr, nc))


def scoring(i, j):
    global ans, find
    numbering = visited[i][j]
    how = team_info[numbering - 1]
    team = team_lst[numbering - 1]
    for w in range(how):  # 점수 찾기
        state, (r, c) = team[w]
        if (r, c) == (i, j) and 1 <= state <= 3:
            ans += (w + 1) * (w + 1)
            find = True
            break
    tmp = []  # 머리. 꼬리 회전
    for w in range(how - 1, -1, -1):  # 3,2,1 순으로 담기
        tmp.append(team[w])
    for w in range(len(team) - 1, how - 1, -1):  # 4도 거꾸로부터 담기
        tmp.append(team[w])

    tmp[0][0] = 1  # 머리!
    for w in range(1, 1 + how - 2):
        tmp[w][0] = 2  # 몽통!
    tmp[how - 1][0] = 3  # 꼬리!
    team_lst[numbering - 1] = tmp  # 반영


n, team_num, order_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
team_lst = []
visited = [[0] * n for i in range(n)]
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]  # 북 동 남 서
team_info = []  # 팀마다 몇명있는지
team_numbering = 1
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1 and not visited[i][j]:
            tmp = []
            visited[i][j] = team_numbering
            tr, tc = bfs(i, j, team_numbering)  # 1,2  담음
            visited[tr][tc] = team_numbering  # 3 담음
            tmp.append([3, (tr, tc)])
            bfs4(tr, tc, team_numbering)  # 4 만 담음
            team_lst.append(tmp)
            team_numbering += 1

ans = 0

for order in range(order_num):

    # 1. 각 팀이 방향에 따라 한칸씩 이동
    for i in range(team_num):
        team = team_lst[i]
        team.insert(0, team.pop())

    # 1-1. 바뀐 위치에 따라 머리, 몸통, 꼬리 반영
    for i in range(team_num):
        how = team_info[i]
        team_lst[i][0][0] = 1
        for j in range(1, 1 + how - 2):
            team_lst[i][j][0] = 2
        team_lst[i][how - 1][0] = 3
        for j in range(how, len(team_lst[i])):
            team_lst[i][j][0] = 4

    # 1-2. 토대로 맵도 변경
    new_grid = [[0] * n for _ in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state

    # 2. 공을 던짐
    # 3. 공맞은 팀 점수 추가
    mok = order // n
    if mok % 4 == 0:  # 가로로 탐색 0 부터
        idx = order % n
        for j in range(n):
            find = False
            if 1 <= new_grid[idx][j] <= 3:
                # 맞았다!
                scoring(idx, j)
            if find:
                break
    if mok % 4 == 2:  # 가로로 탐색 뒤 부터
        idx = n - order % n - 1
        for j in range(n - 1, -1, -1):
            find = False
            if 1 <= new_grid[idx][j] <= 3:
                # 맞았다!
                scoring(idx, j)
            if find:
                break

    if mok % 4 == 3:  # 세로로 탐색 0 부터
        jdx = n - order % n - 1
        for i in range(n):
            find = False
            if 1 <= new_grid[i][jdx] <= 3:
                # 맞았다!
                scoring(i, jdx)
            if find:
                break

    if mok % 4 == 1:  # 세로로 탐색 n 부터
        jdx = order % n
        for i in range(n - 1, -1, -1):
            find = False
            if 1 <= new_grid[i][jdx] <= 3:
                scoring(i, jdx)
            if find:
                break

    # 맞아서 위치 바뀌거 다시 반영!
    new_grid = [[0] * n for _ in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state

    grid = new_grid

print(ans)
