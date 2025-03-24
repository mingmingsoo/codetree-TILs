'''
실제 시험이라고 생각하자.
문제 설명
    1. 인접한 4개 칸 중 나무가 있는 칸 수만큼 나무 성장
    2. 인접한 4개 칸 중 벽/다른나무/제초제 모두 없는 칸에 번식
        칸 갯수 // 만큼
    3. 제초제 뿌림
        4개 대각선으로 k만큼 전파 쭉쭊쭉 -> 멈추는 로직 필요
        우선순위
        (1) 가장 많은 나무
        (2) 행 열 작은 순
        -> 주의!! 나무가 없는칸에선 계산하면 안됨!!!
        제초제는 c년 만큼 남아있다가 c+1년 후에 사라짐.
입력
    맵 n, 박멸이 진행되는 년 수 m, 제초제 확산범위 k, 제초제 남아있는 년수 c
    벽 -1
출력 
    총 박멸한 나무 그루 수
구상
필요한 함수
    1. grow()
    2. spread()
    3. kill()
필요한 변수
    제초제는 따로 2차원 배열로 관리.

테케
전부 박멸되는 경우

5 2 2 1
-1 -1 -1 -1 -1
-1 -1 -1 -1 -1
-1 -1 -1 -1 -1
-1 -1 -1 -1 -1
-1 -1 -1 -1 5


년수 잘 되는지
5 5 2 5
0 0 0 0 0
0 30 23 0 0
0 0 -1 0 0
0 0 17 46 77
0 0 0 12 0

제초제 잘 되는지 검증
5 1 2 1
0 0 0 0 0
0 9 0 9 0
0 0 9 0 0
0 9 0 9 0
-1 0 0 0 0
'''

n, total_time, dist, spray = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
ans = 0
kill_grid = [[0] * n for i in range(n)]

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def grow():  # 제초제 당한애들은 이미 grid가 0임
    plus_grid = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                rnd = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 0:
                        rnd += 1
                plus_grid[i][j] = rnd

    for i in range(n):
        for j in range(n):
            grid[i][j] += plus_grid[i][j]


def spread():
    plus_grid = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                empty = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and \
                            grid[nr][nc] == 0 and kill_grid[nr][nc] == 0:
                        empty += 1
                if empty:
                    growth = grid[i][j] // empty
                    for k in range(4):
                        nr = i + row[k]
                        nc = j + col[k]
                        if 0 <= nr < n and 0 <= nc < n and \
                                grid[nr][nc] == 0 and kill_grid[nr][nc] == 0:
                            plus_grid[nr][nc] += growth

    for i in range(n):
        for j in range(n):
            grid[i][j] += plus_grid[i][j]


row2 = [-1, -1, 1, 1]
col2 = [-1, 1, -1, 1]

ans = 0


def kill():
    global ans
    kill_lst = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:  # 이 조건 의심 필요
                kill_cnt = grid[i][j]
                ele_kill = [(i, j)]
                for k in range(4):
                    for l in range(1, dist + 1):
                        nr = i + row2[k] * l
                        nc = j + col2[k] * l
                        if not (0 <= nr < n and 0 <= nc < n):
                            break
                        if grid[nr][nc] != -1:
                            kill_cnt += grid[nr][nc]
                            ele_kill.append((nr, nc))
                        if grid[nr][nc] <= 0:  # 검증 필요 0인곳 제초제 뿌리는지 확인 필요
                            break
                kill_lst.append((-kill_cnt, (i, j), ele_kill))
    if kill_lst:
        kill_lst.sort()
        kill_cnt, (r, c), location = kill_lst[0]
        ans += abs(kill_cnt)

        for r, c in location:
            kill_grid[r][c] = spray + 1
            grid[r][c] = 0


for time in range(total_time):
    grow()
    # print("---성장---")
    # for _ in grid:
    #     print(_)
    spread()
    # print("---번식---")
    # for _ in grid:
    #     print(_)
    kill()
    # print("---제초제 뿌랴!---")
    # for _ in kill_grid:
    #     print(_)
    # 1씩 감소
    for i in range(n):
        for j in range(n):
            if kill_grid[i][j]:
                kill_grid[i][j] -= 1
    # print("---나무 죽은 후 ---")
    # for _ in grid:
    #     print(_)
    # print("---제초제 감소---")
    # for _ in kill_grid:
    #     print(_)
print(ans)
