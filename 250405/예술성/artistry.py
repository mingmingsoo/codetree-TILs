'''
변의 갯수 구하기
'''
from collections import deque, defaultdict

n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
score = 0


def bfs(r, c):
    mynum = grid[r][c]
    cnt = 0
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        cnt += 1
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] != mynum:
                continue
            visited[nr][nc] = num
            q.append((nr, nc))

    num_info[num] = (mynum, cnt)


def rotation(grid):  # 반시계
    ro_grid = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            ro_grid[i][j] = grid[j][n - i - 1]
    return ro_grid


def srotation(s, r1, c1):
    ro_s = [[0] * (n // 2) for i in range(n // 2)]
    for i in range(n // 2):
        for j in range(n // 2):
            ro_s[i][j] = s[n // 2 - j - 1][i]

    for i in range(n // 2):
        for j in range(n // 2):
            ro_grid[i + r1][j + c1] = ro_s[i][j]


for t in range(4):
    num_info = {}
    face_dict = defaultdict(int)

    num = 1
    visited = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                visited[i][j] = num
                bfs(i, j)
                num += 1

    # 변 갯수 구하기
    for i in range(n):
        for j in range(n):
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] == visited[i][j]:
                    continue
                tmp = [visited[i][j], visited[nr][nc]]
                tmp.sort()
                face_dict[tuple(tmp)] += 1

    # 점수 계산
    for k, v in face_dict.items():
        num1, num2 = k
        face = v // 2
        score += (num_info[num1][1] + num_info[num2][1]) * num_info[num1][0] * num_info[num2][0] * face
    if t == 3:
        break
    # 회전
    # 1. 십자가 회전
    ro_grid = rotation(grid)
    # 2. 작은 회전
    s1 = [_[:n // 2] for _ in grid[:n // 2]]
    s2 = [_[n // 2 + 1:] for _ in grid[:n // 2]]
    s3 = [_[:n // 2] for _ in grid[n // 2 + 1:]]
    s4 = [_[n // 2 + 1:] for _ in grid[n // 2 + 1:]]

    srotation(s1, 0, 0)
    srotation(s2, 0, n // 2 + 1)
    srotation(s3, n // 2 + 1, 0)
    srotation(s4, n // 2 + 1, n // 2 + 1)
    grid = ro_grid
print(score)
