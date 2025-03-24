'''
어려운뎀..


문제설명
    1. 각 팀이 방향에 따라 한칸씩 이동
    2. 공을 던짐
    3. 공맞은 팀 점수 추가
    4. 공맞은 팀은 방향 전환

입력
    맵 n, 팀 m, 라운드 k
    1 머리
    2 중간
    3 꼬리
    4 이동선

출력
    점수 총합

구상
    1. 회전시키는 게 어려운데....
        q에 어떻게 넣냐가 어려울 듯
'''
from collections import deque

n, team_num, order_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

team_lst = []
visited = [[0] * n for i in range(n)]
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]  # 북 동 남 서
team_info = []  # 팀마다 몇명있는지
ans = 0


def bfs(sr, sc, team_numbering):
    q = deque([(sr, sc)])
    tr, tc = -1, -1
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


team_numbering = 1

for i in range(n):
    for j in range(n):
        if grid[i][j] == 1 and not visited[i][j]:
            tmp = []
            visited[i][j] = team_numbering
            tr, tc = bfs(i, j, team_numbering)  # 1,2만 담음
            visited[tr][tc] = team_numbering
            tmp.append([3, (tr, tc)])
            bfs4(tr, tc, team_numbering)  # 4 만 담음
            team_lst.append(tmp)
            team_numbering += 1

# for team in team_lst:
#     print(team)
team_numbering -= 1

for order in range(order_num):
    # pass
    # 1. 각 팀이 방향에 따라 한칸씩 이동
    # print("-----이동전-----")
    # for _ in grid:
    #     print(*_)
    for i in range(team_num):
        team = team_lst[i]
        team.insert(0, team.pop())

    for i in range(team_num):
        how = team_info[i]
        team_lst[i][0][0] = 1
        for j in range(1, 1 + how - 2):
            team_lst[i][j][0] = 2
        team_lst[i][how - 1][0] = 3
        for j in range(how, len(team_lst[i])):
            team_lst[i][j][0] = 4

    # print("------------")
    # for _ in team_lst:
    #     print(_)

    new_grid = [[0] * n for _ in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state
    # print("-------이동후 ")
    # for _ in new_grid:
    #     print(*_)

    # 2. 공을 던짐
    # 3. 공맞은 팀 점수 추가
    mok = order // n
    if mok % 4 == 0:  # 가로로 탐색 0 부터
        idx = order % n
        # print("가로로 탐색 0부터 ", idx)
        for j in range(n):
            find = False
            if 1 <= new_grid[idx][j] <= 3:
                # 맞았다!
                numbering = visited[idx][j]
                how = team_info[numbering - 1]
                team = team_lst[numbering - 1]
                for i in range(how):
                    state, (r, c) = team[i]
                    if (r, c) == (idx, j) and 1 <= state <= 3:
                        ans += (i + 1) * (i + 1)
                        find = True
                        break
                tmp = []
                for i in range(how - 1, -1, -1):
                    tmp.append(team[i])
                for i in range(len(team) - 1, how - 1, -1):
                    tmp.append(team[i])

                tmp[0][0] = 1
                for j in range(1, 1 + how - 2):
                    tmp[j][0] = 2
                tmp[how - 1][0] = 3
                for j in range(how, len(tmp)):
                    tmp[j][0] = 4  # 이건 안해도 되겠지만 일단 두겟음

                team_lst[numbering - 1] = tmp
            if find:
                break
    if mok % 4 == 2:  # 가로로 탐색 뒤 부터
        idx = n - order % n - 1
        # print("가로로 탐색 n부터", idx)
        for j in range(n - 1, -1, -1):
            find = False
            if 1 <= new_grid[idx][j] <= 3:
                # 맞았다!
                numbering = visited[idx][j]
                how = team_info[numbering - 1]
                team = team_lst[numbering - 1]
                for i in range(how):
                    state, (r, c) = team[i]
                    if (r, c) == (idx, j) and 1 <= state <= 3:
                        ans += (i + 1) * (i + 1)
                        find = True
                        break
                tmp = []
                for i in range(how - 1, -1, -1):
                    tmp.append(team[i])
                for i in range(len(team) - 1, how - 1, -1):
                    tmp.append(team[i])

                tmp[0][0] = 1
                for j in range(1, 1 + how - 2):
                    tmp[j][0] = 2
                tmp[how - 1][0] = 3
                for j in range(how, len(tmp)):
                    tmp[j][0] = 4  # 이건 안해도 되겠지만 일단 두겟음

                team_lst[numbering - 1] = tmp
            if find:
                break

    if mok % 4 == 3:  # 세로로 탐색 0 부터
        jdx = n - order % n - 1
        # print("세로로 탐색 0부터", jdx)
        for i in range(n):
            find = False
            if 1 <= new_grid[i][jdx] <= 3:
                # 맞았다!
                numbering = visited[i][jdx]
                how = team_info[numbering - 1]
                team = team_lst[numbering - 1]
                for w in range(how):
                    state, (r, c) = team[w]
                    if (r, c) == (i, jdx) and 1 <= state <= 3:
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
                tmp = []
                for w in range(how - 1, -1, -1):
                    tmp.append(team[w])
                for w in range(len(team) - 1, how - 1, -1):
                    tmp.append(team[w])

                tmp[0][0] = 1
                for w in range(1, 1 + how - 2):
                    tmp[w][0] = 2
                tmp[how - 1][0] = 3
                for w in range(how, len(tmp)):
                    tmp[w][0] = 4  # 이건 안해도 되겠지만 일단 두겟음

                team_lst[numbering - 1] = tmp
            if find:
                break

    if mok % 4 == 1:  # 세로로 탐색 n 부터
        jdx = order % n
        # print("세로로 탐색 n부터", jdx)
        for i in range(n - 1, -1, -1):
            find = False
            if 1 <= new_grid[i][jdx] <= 3:
                # 맞았다!
                numbering = visited[i][jdx]
                how = team_info[numbering - 1]
                team = team_lst[numbering - 1]
                for w in range(how):
                    state, (r, c) = team[w]
                    if (r, c) == (i, jdx) and 1 <= state <= 3:
                        ans += (w + 1) * (w + 1)
                        find = True
                        break
                tmp = []
                for w in range(how - 1, -1, -1):
                    tmp.append(team[w])
                for w in range(len(team) - 1, how - 1, -1):
                    tmp.append(team[w])

                tmp[0][0] = 1
                for w in range(1, 1 + how - 2):
                    tmp[w][0] = 2
                tmp[how - 1][0] = 3
                for w in range(how, len(tmp)):
                    tmp[w][0] = 4  # 이건 안해도 되겠지만 일단 두겟음

                team_lst[numbering - 1] = tmp
            if find:
                break

    new_grid = [[0] * n for _ in range(n)]
    for team in team_lst:
        for state, (r, c) in team:
            new_grid[r][c] = state
    # for _ in new_grid:
    #     print(*_)
    # print(ans)
    grid = new_grid
# 4. 공맞은 팀은 방향 전환
print(ans)
