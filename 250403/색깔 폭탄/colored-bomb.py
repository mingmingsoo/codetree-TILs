'''아마 16:42 부터?
문제 설명
    1. 0은 어디에나 가능 -> bfs안에서 visited
    2. 색깔 있는 곳(빨 제외)에서만 bfs -> 총 2 개 이상
    3. 우선순위 주의
입력
    맵 크기 n, 색깔 몇개인지 m
    맵 정보
출력
    터지는 크기**2 합
'''
from collections import deque

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
score = 0


def myprint():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 6:
                print(" ", end=" ")
            elif grid[i][j] == -1:
                print("B", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()


def rotation():
    grid_origin = [_[:] for _ in grid]
    for i in range(n):
        for j in range(n):
            grid[i][j] = grid_origin[j][n - i - 1]


def gravity():
    for j in range(n):
        while True:
            down = False
            for i in range(n - 1, 0, -1):
                if grid[i][j] == 6 and 0 <= grid[i - 1][j] <= 5:
                    down = True
                    grid[i][j], grid[i - 1][j] = grid[i - 1][j], grid[i][j]
            if not down:
                break


def bfs(r, c):
    cnt = 0
    red = 0
    location = []
    visited[r][c] = True
    q = deque([(r, c)])
    red_visited = set()
    color = grid[r][c]
    while q:
        r, c = q.popleft()
        cnt += 1
        if grid[r][c] == 0: red += 1
        location.append((r, c))

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if not visited[nr][nc] and grid[nr][nc] == color:
                q.append((nr, nc))
                visited[nr][nc] = True
            if (nr, nc) not in red_visited and grid[nr][nc] == 0:
                q.append((nr, nc))
                red_visited.add((nr, nc))

    if cnt > 1:
        return cnt, red, location
    else:
        return -1, -1, -1


while True:

    bomb_lst = []
    visited = [[False] * n for i in range(n)]

    row = [-1, 1, 0, 0]
    col = [0, 0, 1, -1]

    for i in range(n - 1, -1, -1):
        for j in range(n):
            if 0 < grid[i][j] < 6 and not visited[i][j]:  # 검, 빨 제외
                total, red, location = bfs(i, j)
                if total != -1:
                    bomb_lst.append((-total, red, -i, j, location))

    if bomb_lst:
        bomb_lst.sort()
        cnt, lo = bomb_lst[0][0], bomb_lst[0][4]
        score += cnt ** 2
        # 6 이 빈공간
        for br, bc in lo:
            grid[br][bc] = 6
    else:
        break

    gravity()
    rotation()
    gravity()

print(score)
