''''
코드 리팩토링: 작은애들 회전 함수화

문제설명
    1. 넘버링
    2. 맞닿은 변 갯수 구하기 (이게 좀 ..)
    3. 회전 (이건 뭐 열심히...)
구상
    맞닿은 변 갯수 구하는게 문제인데
    3턴만 있으니까
    총 그룹핑된 갯수의 2개씩의 조합을 딕셔너리로 구해놓고
    +=1 해주고
    두번 다시 안더해지게 visited 방향을 담아서 좌우/상하 다 트루쳐버린다
'''
from collections import deque


def small_rotate(r1, r2, c1, c2, grid_copy):
    small_grid = [_[c1:c2] for _ in grid_copy[r1:r2]]
    small_ro_grid = [_[:] for _ in small_grid]
    for i in range(sn):
        for j in range(sn):
            small_grid[i][j] = small_ro_grid[sn - j - 1][i]

    for i in range(sn):
        for j in range(sn):
            grid[i + r1][j + c1] = small_grid[i][j]


def rotation():
    grid_copy = [_[:] for _ in grid]  # 얘가 원본
    for i in range(n):
        for j in range(n):
            grid[i][j] = grid_copy[j][n - i - 1]

    # 작은 애들
    small_rotate(0, n // 2, 0, n // 2, grid_copy)
    small_rotate(0, n // 2, n // 2 + 1, n, grid_copy)
    small_rotate(n // 2 + 1, n, 0, n // 2, grid_copy)
    small_rotate(n // 2 + 1, n, n // 2 + 1, n, grid_copy)


def bfs(r, c, same_num, number):
    q = deque([(r, c)])
    cnt = 0
    while q:
        r, c = q.popleft()
        cnt += 1
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or numbering_map[nr][nc] or grid[nr][nc] != same_num:
                continue
            numbering_map[nr][nc] = number
            q.append((nr, nc))
    return cnt


def combi(sidx, idx):
    if sidx == 2:
        if numbering_match[sel[0]] != numbering_match[sel[1]]:
            score_dict[tuple(sel)] = 0
        return
    if idx == number + 1:
        return
    sel[sidx] = idx
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


n = int(input())
sn = n // 2
grid = [list(map(int, input().split())) for i in range(n)]
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
ans = 0
for i in range(4):
    numbering_map = [[0] * n for i in range(n)]  # 이게 visited 처럼 쓰일 거임
    number = 1

    numbering_match = {}
    numbering_have = {}

    for i in range(n):
        for j in range(n):
            if not numbering_map[i][j]:
                numbering_map[i][j] = number
                cnt = bfs(i, j, grid[i][j], number)
                numbering_match[number] = grid[i][j]
                numbering_have[number] = cnt
                number += 1

    number -= 1

    # 점수 계산할 조합 만들기
    score_dict = {}
    sel = [0] * 2

    combi(0, 1)

    # 변의 갯수 샌다.
    visited = [[[False] * 4 for i in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            my_num = numbering_map[i][j]
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if not (0 <= nr < n and 0 <= nc < n):
                    continue
                other_num = numbering_map[nr][nc]
                if not visited[i][j][k] and not visited[nr][nc][(k + 2) % 4] and other_num != my_num:
                    tmp = [my_num, other_num]
                    tmp.sort()
                    score_dict[tuple(tmp)] += 1
                    visited[i][j][k] = True
                    visited[nr][nc][(k + 2) % 4] = True

    for key, value in score_dict.items():
        if value:
            team1 = key[0]
            team2 = key[1]
            team1_have = numbering_have[team1]
            team2_have = numbering_have[team2]
            tem1_num = numbering_match[team1]
            tem2_num = numbering_match[team2]
            ans += (team1_have + team2_have) * tem1_num * tem2_num * value
    if i == 3:
        break  # 여까지 왔으면 마지막 회전 안해도 된다.
    rotation()
print(ans)
