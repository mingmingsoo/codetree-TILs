'''
문제 설명
    - 머리 따라 이동
        dict에 담기
        머리 pop 하고 꼬리 찾고 4 or 3
        그 다음에 다시 insert
        그거 기반 맵 반영
    - 공 굴려 위해서 넘버링 필요
        반전
입력
    맵 n 팀 m 라운드 수 k
1-3 일수가 있나..? 일단 없다고 가정..

5 1 1
1 2 2 2 2
3 0 0 0 2
2 0 0 0 2
2 0 0 0 2
2 2 2 2 2


'''
from collections import defaultdict, deque

n, tn, turn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
# 넘버링
num_map = [[0] * n for i in range(n)]
num = 1
team_info = defaultdict(list)
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(r, c):
    team_info[num].append((r, c))  # 머리 담기
    q = deque([(r, c, 1)])  # 머리
    while q:
        r, c, position = q.popleft()

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or num_map[nr][nc] or not grid[nr][nc]:
                continue
            if position == 1:
                if grid[nr][nc] == 2:  # 2만 찾아!
                    team_info[num].append((nr, nc))
                    q.append((nr, nc, grid[nr][nc]))
                    num_map[nr][nc] = num
            else:
                if 2 <= grid[nr][nc] <= 3:
                    team_info[num].append((nr, nc))
                    q.append((nr, nc, grid[nr][nc]))
                    num_map[nr][nc] = num
                elif grid[nr][nc] == 4:
                    q.append((nr, nc, grid[nr][nc]))
                    num_map[nr][nc] = num


for i in range(n):
    for j in range(n):
        if grid[i][j] == 1 and not num_map[i][j]:
            num_map[i][j] = num
            bfs(i, j)
            num += 1
score = 0
for t in range(turn):

    # 1. 머리 따라서 이동
    for k, v in team_info.items():
        hr, hc = v[0]
        tr, tc = v.pop()  # 꼬리 빼
        grid[tr][tc] = 4

        # 머리 찾아
        for k in range(4):
            nr = hr + row[k]
            nc = hc + col[k]
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] in (3, 4):
                v.insert(0, (nr, nc))
                grid[nr][nc] = 1
                break
        # 기반 맵 반영

        for i in range(1, len(v) - 1):
            r, c = v[i]
            grid[r][c] = 2
        grid[v[len(v) - 1][0]][v[len(v) - 1][1]] = 3

    if (t // n) % 4 == 0:
        mod = t % n
        # print(t, (t // n) % 4,  mod)
        find = False
        for j in range(n):
            if 1 <= grid[mod][j] <= 3:  # 공 발견!!
                team_num = num_map[mod][j]
                for idx, location in enumerate(team_info[team_num]):
                    r, c = location
                    if (r, c) == (mod, j):
                        score += (idx + 1) ** 2
                        team_info[team_num].reverse()
                        v = team_info[team_num]
                        grid[v[0][0]][v[0][1]] = 1
                        grid[v[len(v)-1][0]][v[len(v)-1][1]] = 3
                        for tidx in range(1, len(v)-1):
                            grid[v[tidx][0]][v[tidx][1]] = 2


                        find = True
                        break
            if find:
                break
    elif (t // n) % 4 == 1:
        mod = t % n
        # print(t, (t // n) % 4, mod)
        find = False
        for i in range(n - 1, -1, -1):
            if 1 <= grid[mod][i] <= 3:  # 공 발견!!
                team_num = num_map[mod][i]
                for idx, location in enumerate(team_info[team_num]):
                    r, c = location
                    if (r, c) == (mod, i):
                        score += (idx + 1) ** 2
                        team_info[team_num].reverse()
                        v = team_info[team_num]
                        grid[v[0][0]][v[0][1]] = 1
                        grid[v[len(v)-1][0]][v[len(v)-1][1]] = 3
                        for tidx in range(1, len(v)-1):
                            grid[v[tidx][0]][v[tidx][1]] = 2
                        find = True
                        break
            if find:
                break

    elif (t // n) % 4 == 2:
        mod = n - 1 - (t % n)
        # print(t, (t // n) % 4, mod)
        find = False
        for j in range(n - 1, -1, -1):
            if 1 <= grid[mod][j] <= 3:  # 공 발견!!
                team_num = num_map[mod][j]
                for idx, location in enumerate(team_info[team_num]):
                    r, c = location
                    if (r, c) == (mod, j):
                        score += (idx + 1) ** 2
                        team_info[team_num].reverse()
                        v = team_info[team_num]
                        grid[v[0][0]][v[0][1]] = 1
                        grid[v[len(v)-1][0]][v[len(v)-1][1]] = 3
                        for tidx in range(1, len(v)-1):
                            grid[v[tidx][0]][v[tidx][1]] = 2
                        find = True
                        break
            if find:
                break

    elif (t // n) % 4 == 3:
        mod = n - 1 - (t % n)
        # print(t, (t // n) % 4, mod)
        find = False
        for i in range(n):
            if 1 <= grid[mod][i] <= 3:  # 공 발견!!
                team_num = num_map[mod][i]
                for idx, location in enumerate(team_info[team_num]):
                    r, c = location
                    if (r, c) == (mod, i):
                        score += (idx + 1) ** 2
                        team_info[team_num].reverse()
                        v = team_info[team_num]
                        grid[v[0][0]][v[0][1]] = 1
                        grid[v[len(v)-1][0]][v[len(v)-1][1]] = 3
                        for tidx in range(1, len(v)-1):
                            grid[v[tidx][0]][v[tidx][1]] = 2
                        find = True
                        break
            if find:
                break

    # print("----------")
    # for _ in grid:
    #     print(_)
print(score)
