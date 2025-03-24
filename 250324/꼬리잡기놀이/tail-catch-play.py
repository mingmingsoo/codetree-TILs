'''
쉽게 쉽게....
0841~
'''
from collections import deque

n, team_num, turn_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

# 초기 설정
team_list = []
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(sr, sc):
    q = deque([(sr, sc)])
    grid[sr][sc] = team_numbering
    tmp = []
    while q:
        r, c = q.popleft()
        tmp.append((r, c))
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if grid[nr][nc] == 2:
                q.append((nr, nc))
                grid[nr][nc] = team_numbering
            elif grid[nr][nc] == 3 and (r, c) != (sr, sc):
                q.append((nr, nc))
                grid[nr][nc] = team_numbering
    team_list.append(tmp)


team_info = []
team_numbering = 5
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:  # 머리면
            bfs(i, j)
            team_info.append(team_numbering)
            team_numbering += 1
ans = 0
for turn in range(turn_num):
    # 이동
    for idx, team in enumerate(team_list):
        team_num = team_info[idx]
        # 1. 꼬리는 4처리
        tr, tc = team.pop()
        grid[tr][tc] = 4
        # 2. 머리에서 4 찾아서 team_num으로 바꿔주고 q에 맨 앞에 넣어줌
        hr, hc = team[0]
        for k in range(4):
            nr = hr + row[k]
            nc = hc + col[k]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if grid[nr][nc] == 4:
                team.insert(0, (nr, nc))
                grid[nr][nc] = team_num
                break
    # 공
    mok = turn // n
    if mok % 4 == 0:
        idx = turn % n
        for j in range(0, n, 1):
            if grid[idx][j] >= 5:
                team_num = grid[idx][j]
                ans += (team_list[team_num - 5].index((idx, j)) + 1) ** 2
                team_list[team_num - 5].reverse()
                break
    elif mok % 4 == 2:
        idx = n - turn % n - 1
        for j in range(n - 1, -1, -1):
            if grid[idx][j] >= 5:
                team_num = grid[idx][j]
                ans += (team_list[team_num - 5].index((idx, j)) + 1) ** 2
                team_list[team_num - 5].reverse()
                break
    elif mok % 4 == 3:
        jdx = n - turn % n - 1
        for i in range(0, n, 1):
            if grid[i][jdx] >= 5:
                team_num = grid[i][jdx]
                ans += (team_list[team_num - 5].index((i, jdx)) + 1) ** 2
                team_list[team_num - 5].reverse()
                break
    elif mok % 4 == 1:
        jdx = turn % n
        for i in range(n - 1, -1, -1):
            if grid[i][jdx] >= 5:
                team_num = grid[i][jdx]
                ans += (team_list[team_num - 5].index((i, jdx)) + 1) ** 2
                team_list[team_num - 5].reverse()
                break
print(ans)

