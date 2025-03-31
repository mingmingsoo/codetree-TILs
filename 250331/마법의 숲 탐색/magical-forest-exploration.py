'''
틀린이유: 왼/오가 if elif가 아니라 if, if 여야함 ㅠㅠ
        전에 코드는 왼쪽으로만 가는 코드...
문제설명
    1. 정령은 위에서 내려옴
        중앙, 위, 아래, 왼, 오, 방향 관리
    2.  while True:
            남쪽으로 쭉
            오른쪽/왼쪽 한칸
                오/왼 못가면 break
            break 조건은?
    3. 정령 이동
            골렘을 넘버링.
            출구를 -1로 기록
            내 넘버는 어디든 갈 수 있고
            출구로는 어디로든지 갈 수 있음
입력
    맵 크기 n,m, 정령수 player_num
    골렘 출발 열, 방향
    0 1 2 3
    북동남서
출력
    매 턴마다 정령 위치 합
필요한 변수
    idx, r,c,d: 골렘 넘버, 중앙, 방향
    grid: 골렘 2차원 배열 기록(출구 -1)
필요한 함수
    down()
    left()
    right()
    bfs()
    clear()
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
        change = False
        down()

        # 위 r-1, c -> r-1, c-1
        # 왼 r, c-1 -> r, c-2
        # 밑 r+1, c -> r+1, c-1
        if c - 1 > 0 and grid[r - 1][c - 1] == grid[r][c - 2] == grid[r + 1][c - 1] == 0:
            if r + 1 < n - 1 and grid[r + 1][c - 2] == grid[r + 2][c - 1] == 0:
                c -= 1
                r += 1
                d = (d - 1) % 4
                change = True
        # 위 r-1, c -> r-1, c+1
        # 오 r, c+1 -> r, c+2
        # 밑 r+1, c -> r+1, c+1
        if c + 1 < m - 1 and grid[r - 1][c + 1] == grid[r][c + 2] == grid[r + 1][c + 1] == 0:
            if r + 1 < n - 1 and grid[r + 1][c + 2] == grid[r + 2][c + 1] == 0:
                r += 1
                c += 1
                d = (d + 1) % 4
                change = True
        if not change:  # 못움직여요!
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
