'''
문제설명
    2차원배열이 있을때
    상하좌우 인접한 칸과 내 차이가 기준에 해당하면 합쳐준다.
    -> 넘버링 필요...
    계란 이동이 없을떄까지 반복한다.

구상
    bfs로 넘버링 한다.
    넘버링 후 계산.
출력 계란의 이동이 일어난 총 횟수
'''
from collections import deque

n, small, big = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
time = 0
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs(r, c, numbering):
    q = deque([(r, c)])
    cnt = 0
    location = set()
    summ = 0
    while q:
        r, c = q.popleft()

        location.add((r, c))
        summ += grid[r][c]
        cnt += 1
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if visited[nr][nc] == 0 and small <= abs(grid[r][c] - grid[nr][nc]) <= big:
                visited[nr][nc] = numbering
                q.append((nr, nc))

    ele_num = summ // cnt
    for r, c in location:
        new_grid[r][c] = ele_num


while True:

    # 넘버링,
    visited = [[0] * n for i in range(n)]
    numbering = 1
    new_grid = [_[:] for _ in grid]
    for i in range(n):
        for j in range(n):
            if visited[i][j] == 0:
                visited[i][j] = numbering
                bfs(i, j, numbering)
                numbering += 1
    if grid == new_grid:
        break
    else:
        grid = new_grid
    time += 1

print(time)
