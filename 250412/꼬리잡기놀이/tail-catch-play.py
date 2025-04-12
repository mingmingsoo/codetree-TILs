'''
문제 설명
    1. 머리따라서 이동
    2. 라운드에 따라 공 굴림
    3. 공 맞은 팀 점수 획득
    4. 공 맞은 팀은 반대가 됨

필요한 함수
    bfs - 팀 정보 찾음
필요한 변수
    team_info : 팀 정보 딕셔너리
    number_map : 팀 넘버링 맵
입력
    맵 크기 n, 팀 갯수 m, 라운드 수 k
3 1 5
1 2 2
3 0 2
2 2 2
'''
from collections import defaultdict, deque

n, tn, turn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
number_map = [[0] * n for i in range(n)]
team_info = defaultdict(list)

num = 1
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
score = 0


def bfs(r, c):
    q = deque([(r, c, 1)])
    team_info[num].append((r, c))
    number_map[r][c] = num
    while q:
        r, c, position = q.popleft()
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or number_map[nr][nc] or not grid[nr][nc]:
                continue
            if position == 1 and grid[nr][nc] == 2:
                q.append((nr, nc, grid[nr][nc]))
                team_info[num].append((nr, nc))
                number_map[nr][nc] = num
            if position != 1 and grid[nr][nc] in (2, 3):
                q.append((nr, nc, grid[nr][nc]))
                team_info[num].append((nr, nc))
                number_map[nr][nc] = num
            if position != 1 and grid[nr][nc] == 4:
                q.append((nr, nc, grid[nr][nc]))
                number_map[nr][nc] = num


for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            bfs(i, j)
            num += 1

for t in range(turn):

    #     1. 머리따라서 이동
    for k, v in team_info.items():
        tr, tc = v.pop()
        grid[tr][tc] = 4
        hr, hc = v[0]
        grid[hr][hc] = 2
        nhr, nhc = hr, hc
        for k in range(4):
            nr = hr + row[k]
            nc = hc + col[k]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if grid[nr][nc] in (3, 4):
                nhr, nhc = nr, nc
                break
        v.insert(0, (nhr, nhc))
        grid[nhr][nhc] = 1
        grid[v[-1][0]][v[-1][1]] = 3


    #     2. 라운드에 따라 공 굴림
    if (t // n) % 4 == 0:
        idx = t % n
        # print(t, (t // n) % 4, idx)
        for j in range(n):
            if 1 <= grid[idx][j] <= 3:
                team = number_map[idx][j]
                tdx = team_info[team].index((idx, j))
                score += (tdx + 1) ** 2
                team_info[team].reverse()
                hr, hc = team_info[team][0]
                tr, tc = team_info[team][-1]
                grid[hr][hc] = 1
                grid[tr][tc] = 3
                break

    elif (t // n) % 4 == 1:
        jdx = t % n
        # print(t, (t // n) % 4, jdx)
        for i in range(n - 1, -1, -1):
            if 1 <= grid[i][jdx] <= 3:
                team = number_map[i][jdx]
                tdx = team_info[team].index((i, jdx))
                score += (tdx + 1) ** 2
                team_info[team].reverse()
                hr, hc = team_info[team][0]
                tr, tc = team_info[team][-1]
                grid[hr][hc] = 1
                grid[tr][tc] = 3
                break
    elif (t // n) % 4 == 2:
        idx = n - 1 - t % n
        # print(t, (t // n) % 4, idx)
        for j in range(n - 1, -1, -1):
            if 1 <= grid[idx][j] <= 3:
                team = number_map[idx][j]
                tdx = team_info[team].index((idx, j))
                score += (tdx + 1) ** 2
                team_info[team].reverse()
                hr, hc = team_info[team][0]
                tr, tc = team_info[team][-1]
                grid[hr][hc] = 1
                grid[tr][tc] = 3
                break
    elif (t // n) % 4 == 3:
        jdx = n - 1 - t % n
        # print(t, (t // n) % 4, jdx)
        for i in range(n):
            if 1 <= grid[i][jdx] <= 3:
                team = number_map[i][jdx]
                tdx = team_info[team].index((i, jdx))
                score += (tdx + 1) ** 2
                team_info[team].reverse()
                hr, hc = team_info[team][0]
                tr, tc = team_info[team][-1]
                grid[hr][hc] = 1
                grid[tr][tc] = 3
                break

print(score)
