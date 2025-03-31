'''
실험쓰
'''
# ------------------------- 입력 -------------------------
from collections import deque

n, m, player_num = map(int, input().split())
n += 3  # 위로 3개 패딩
grid = [[0] * m for i in range(n)]
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]


# ------------------------- 함수 -------------------------
def down():
    global r, c
    while True:
        if r + 1 < n - 1 and grid[r + 1][c - 1] == grid[r + 1][c + 1] == grid[r + 2][c] == 0:
            r += 1
        else:
            break


def clear():
    for i in range(3):
        for j in range(m):
            if grid[i][j]:
                return True
    return False


def bfs():
    global r, c
    # 중앙은 r,c임
    visited = [[False] * m for i in range(n)]
    visited[r][c] = True
    q = deque([(r, c, grid[r][c])])

    while q:
        qr, qc, num = q.popleft()
        r = max(r, qr)  # 얼만큼 내려갈 수 있니
        for k in range(4):
            nr = qr + row[k]
            nc = qc + col[k]
            if not (0 <= nr < n and 0 <= nc < m) or visited[nr][nc]:
                continue
            if abs(grid[nr][nc]) == num:  # 같은 곳으로는 어디든 갈 수 이쏘...
                visited[nr][nc] = True
                q.append((nr, nc, num))
            elif grid[nr][nc] and grid[nr][nc] != num and grid[qr][qc] == -num:
                visited[nr][nc] = True
                q.append((nr, nc, abs(grid[nr][nc])))  # 탈출구까지 겹칠 수 있어서..


# ------------------------- 메인 -------------------------
ans = 0
for p in range(player_num):
    c, d = map(int, input().split())
    c -= 1
    r = 0  # 맨 처음 중앙은 격자밖
    while True:
        down()
        # 위 r-1, c -> r-1, c-1
        # 왼 r, c-1 -> r, c-2
        # 밑 r+1, c -> r+1, c-1
        if c - 1 > 0 and r + 1 < n - 1 and grid[r - 1][c - 1] == grid[r][c - 2] == grid[r + 1][c - 1] == grid[r + 1][
            c - 2] == grid[r + 2][c - 1] == 0:
            c -= 1
            r += 1
            d = (d - 1) % 4
        # 위 r-1, c -> r-1, c+1
        # 오 r, c+1 -> r, c+2
        # 밑 r+1, c -> r+1, c+1
        elif c + 1 < m - 1 and r + 1 < n - 1 and grid[r - 1][c + 1] == grid[r][c + 2] == grid[r + 1][c + 1] == \
                grid[r + 1][c + 2] == grid[r + 2][c + 1] == 0:
            r += 1
            c += 1
            d = (d + 1) % 4
        else:
            break

    grid[r][c] = grid[r - 1][c] = grid[r + 1][c] = grid[r][c - 1] = grid[r][c + 1] = p + 1  # 정령 표시

    if clear():  # 초기화!
        grid = [[0] * m for i in range(n)]
        continue

    # 탈출구 표시
    exit = {0: (r - 1, c), 1: (r, c + 1), 2: (r + 1, c), 3: (r, c - 1)}
    grid[exit[d][0]][exit[d][1]] = -(p + 1)
    bfs()
    ans += (r - 2)

print(ans)
