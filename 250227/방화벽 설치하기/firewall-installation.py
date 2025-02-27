'''
문제설명
    방화벽을 3개까지 추가로 설치할 수 있을 때
    불이 안번지는 최대 갯수는?
입력
    맵크기
    2 불 1 벽 0 퍼질 수 있음
구상
    3개 선택은 조합으로 하고
    모든 경우의 수에서 bfs로 돌리기
필요한 메서드
    combi : 방 3 개 조합
    bfs : 불 퍼짐
    count : 불이 안퍼지는 갯수 세기 -> ans 갱신 필요
'''
from collections import deque

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

location_arr = []
location_sel = [0] * 3  # 벽 3개만
origin_q = deque()
for i in range(n):
    for j in range(m):
        if grid[i][j] == 0:
            location_arr.append((i, j))
        elif grid[i][j] == 2:
            origin_q.append((i, j))

ans = 0


def count(grid):
    no_fire = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                no_fire += 1

    return no_fire


row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(q):
    while q:
        r, c = q.popleft()

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < m):
                continue

            if grid[nr][nc] == 0:
                grid[nr][nc] = 2
                q.append((nr, nc))  # visited 굳이 필요 없을듯
    # print("--------bfs 끝나고-------")
    # for _ in grid:
    #     print(_)


def combi(sidx, idx):
    global ans, grid

    if sidx == 3:
        grid_copy = [_[:] for _ in grid]

        q = origin_q.copy()  # 여기서,,, 에러
        for r, c in location_sel:
            grid[r][c] = 1  # 방화벽처리.

        bfs(q)
        # for _ in grid:
        #     print(_)
        ans = max(count(grid), ans)
        grid = [_[:] for _ in grid_copy]

        return
    if idx == len(location_arr):
        return

    location_sel[sidx] = location_arr[idx]
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


combi(0, 0)

print(ans)
