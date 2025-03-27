'''
교수님 코드 손민수
3차원 배열일 필요가 없다.
플레이어가 같은 곳에 가면 앞으로는 쭉 이동경로가 같기 때문

어우 근데 초반 입력에 같은 위치인 애들이 들어올 수 있구나 ;;ㅋㅋ
'''
# ------------------- 입력 ----------------------------
n, people_num, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
for p in range(people_num):
    r, c = map(int, input().split())
    grid[r - 1][c - 1] -= 1  # 사람을 -1 처리

er, ec = map(lambda x: int(x) - 1, input().split())
grid[er][ec] = 10  # 벽이 10

people_exit = 0  # int로 관리
ans = 0
row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]


# ------------------- 함수 ----------------------------
def move():
    global ans, grid, people_exit
    new_grid = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if grid[i][j] < 0:  # 사람이당!
                move = False
                cur = abs(er - i) + abs(ec - j)
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if not (0 <= nr < n and 0 <= nc < n) or 0 < grid[nr][nc] < 10:  # 벽만 못간다
                        continue
                    next = abs(er - nr) + abs(ec - nc)
                    if next < cur:
                        move = True
                        ans += abs(grid[i][j])
                        if (nr, nc) == (er, ec):  # 만약 출구면 탈출 인원만 증가!
                            people_exit += abs(grid[i][j])
                        else:
                            new_grid[nr][nc] += grid[i][j]  # 아니면 옮겨줘!
                        break
                if not move:
                    new_grid[i][j] += grid[i][j]
            elif grid[i][j] > 0:
                new_grid[i][j] = grid[i][j]  # 벽, 탈출구도 고대로
    grid = new_grid


def rotation():
    global er, ec
    L, R, C = 0, 0, 0
    for length in range(2, n + 1):  # 사각형 크기
        is_length = False
        for r in range(0, n - length + 1):
            for c in range(0, n - length + 1):
                people_have, exit_have = False, False
                # 내가 선택한 사각형
                for i in range(r, r + length):
                    for j in range(c, c + length):
                        if grid[i][j] == 10:  # 탈출구당!
                            exit_have = True
                        if grid[i][j] < 0:  # 사람이당!
                            people_have = True
                if people_have and exit_have:
                    is_length = True
                    L, R, C = length, r, c
                    break
            if is_length:
                break
        if is_length:
            break

    small_grid = [_[C:C + L] for _ in grid[R:R + L]]
    small_lo_grid = [[0] * L for i in range(L)]

    for i in range(L):
        for j in range(L):
            small_lo_grid[i][j] = small_grid[L - j - 1][i]

    for i in range(L):
        for j in range(L):
            if 0 < small_lo_grid[i][j] < 10:  # 벽이당!
                small_lo_grid[i][j] -= 1
            grid[i + R][j + C] = small_lo_grid[i][j]
            if grid[i + R][j + C] == 10:  # 탈출구 갱신!
                er, ec = i + R, j + C


# ------------------- 메인 ----------------------------
for t in range(time):
    move()
    rotation()  # er,ec 갱신 필요
    if people_exit == people_num:  # 다 탈출 했으면 그만~
        break
print(ans)
print(er + 1, ec + 1)
