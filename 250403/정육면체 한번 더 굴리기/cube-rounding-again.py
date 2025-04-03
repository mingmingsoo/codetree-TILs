'''
문제 설명
    - 점수판이 필요하다
    - 주사위 굴린다
      (1) 범위 검사 -> 방향만 바꾸기
      (2) nr, nc 구하고
      (0) 점수
      (3) 아랫면하고 비교 해서 방향 바꾸기
헷갈리는 게 처음 위치에서도 점수 얻는지? ㄴㄴ
처음엔 항상 오른쪽
'''
from collections import deque

n, turn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

score_grid = [[0] * n for i in range(n)]
visited = [[False] * n for i in range(n)]
row = [0, 1, 0, -1]
col = [1, 0, -1, 0]


def bfs(r, c):
    num = grid[r][c]
    q = deque([(r, c)])
    location = set()
    while q:
        r, c = q.popleft()
        location.add((r, c))

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] != num:
                continue
            visited[nr][nc] = True
            q.append((nr, nc))
    sm = num * len(location)

    for r, c in location:
        score_grid[r][c] = sm


for i in range(n):
    for j in range(n):
        if not visited[i][j]:
            visited[i][j] = True
            bfs(i, j)
    #  위 아래 앞  뒤 왼 오
dice = [1, 6, 2, 5, 4, 3]
r = c = d = 0
ans = 0


def rotation():
    global dice
    if d == 0:
        dice = [dice[4], dice[5], dice[2], dice[3], dice[1], dice[0]]
    elif d == 2:
        dice = [dice[5], dice[4], dice[2], dice[3], dice[0], dice[1]]
    elif d == 3:  # 북
        dice = [dice[2], dice[3], dice[1], dice[0], dice[4], dice[5]]
    elif d == 1:  # 남
        dice = [dice[3], dice[2], dice[0], dice[1], dice[4], dice[5]]


for t in range(turn):
    nr = r + row[d]
    nc = c + col[d]
    if not (0 <= nr < n and 0 <= nc < n):
        d = (d + 2) % 4
    nr = r + row[d]
    nc = c + col[d]

    ans += score_grid[nr][nc]
    rotation()

    if dice[1] > grid[nr][nc]:
        d = (d + 1) % 4
    elif dice[1] < grid[nr][nc]:
        d = (d - 1) % 4
    r = nr
    c = nc
print(ans)
