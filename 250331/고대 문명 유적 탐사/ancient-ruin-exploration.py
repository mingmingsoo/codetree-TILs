'''
문제 설명
    5*5, 유물 번호 1~7, 총 K턴
    1. 3*3 격자 90,180,270 회전
        (1) 유물 1차 획득이 높은 순
        (2) 각도가 작은
        (3) 열, 행 작은 순으로 선택
        * 유물 1차 획득은 3개 이상 사라질 수 있는 조각의 총 "갯수"
    2. 사라진 빈 칸에 열 작, 행 큰 순으로 채워줌
        for j in range(n):
            for i in range(n-1,-1,-1):
                if grid[i][j] == 0:~

        popleft 필요

    3. 다시 bfs
        while
            find = False
            bfs()
            if not find:
                break
    4. bfs 발견 못하면 종료
주의할 점
    출력형태 만족하는지 확인
    무조건 회전하는거지? 0도는 없는거지?
1 20
7 6 7 6 7
6 7 6 7 6
6 7 1 5 4
7 9 8 -1 1
5 4 3 2 7
3 2 3 5 2 4 6 1 3 2 5 6 2 1 6 6 7 5 4 2 2 3 1 3 1 2 4 2 1 3

180도 회전이 선택됨
'''
from collections import deque


def rotation(grid):
    ro_grid = [[0] * 3 for i in range(3)]

    for i in range(3):
        for j in range(3):
            ro_grid[i][j] = grid[3 - j - 1][i]

    return ro_grid


def bfs(sr, sc):
    q = deque([(sr, sc)])
    num = grid[sr][sc]
    ele_lo = []
    ele = 0
    while q:
        r, c = q.popleft()
        ele_lo.append((r, c))
        ele += 1
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc] != num:
                continue
            visited[nr][nc] = True
            q.append((nr, nc))
    if ele >= 3:
        ele_location.extend(ele_lo)
        return ele
    else:
        return 0


n = 5
turn_num, fill_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
fill_lst = list(map(int, input().split()))  # 얘가 모자랄 일이 없다는거지?

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]

for turn in range(turn_num):
    ans = 0
    rotation_lst = []
    grid_origin = [_[:] for _ in grid]
    for i in range(n - 2):
        for j in range(n - 2):
            small_grid = [_[j:j + 3] for _ in grid[i:i + 3]]
            ro90 = rotation(small_grid)
            for r in range(3):
                for c in range(3):
                    grid[r + i][c + j] = ro90[r][c]

            visited = [[False] * n for i in range(n)]
            cnt90 = 0
            ele_location = []
            for r in range(n):
                for c in range(n):
                    if not visited[r][c]:
                        visited[r][c] = True
                        cnt90 += bfs(r, c)

            if cnt90 > 0:
                rotation_lst.append((-cnt90, 90, (j + 1, i + 1), ele_location))

            grid = [_[:] for _ in grid_origin]

            ro180 = rotation(ro90)
            for r in range(3):
                for c in range(3):
                    grid[r + i][c + j] = ro180[r][c]

            visited = [[False] * n for i in range(n)]
            cnt180 = 0
            ele_location = []
            for r in range(n):
                for c in range(n):
                    if not visited[r][c]:
                        visited[r][c] = True
                        cnt180 += bfs(r, c)

            if cnt180 > 0:
                rotation_lst.append((-cnt180, 180, (j + 1, i + 1), ele_location))

            grid = [_[:] for _ in grid_origin]

            ro270 = rotation(ro180)
            ele_location = []
            for r in range(3):
                for c in range(3):
                    grid[r + i][c + j] = ro270[r][c]

            visited = [[False] * n for i in range(n)]
            cnt270 = 0
            for r in range(n):
                for c in range(n):
                    if not visited[r][c]:
                        visited[r][c] = True
                        cnt270 += bfs(r, c)

            if cnt270 > 0:
                rotation_lst.append((-cnt270, 270, (j + 1, i + 1), ele_location))

            grid = [_[:] for _ in grid_origin]

    if rotation_lst:
        rotation_lst.sort()
        cnt, degree, (j, i), location = rotation_lst[0]
        ans += abs(cnt)
    else:
        break

    j -= 1
    i -= 1
    # 선택한거 기준으로 grid 실제로 반영
    small_grid = [_[j:j + 3] for _ in grid[i:i + 3]]
    ro_grid = [[0] * 3 for i in range(3)]
    for ro in range(0, degree, 90):
        ro_grid = rotation(small_grid)
        small_grid = [_[:] for _ in ro_grid]

    for r in range(3):
        for c in range(3):
            grid[r + i][c + j] = ro_grid[r][c]

    for lr, lc in location:
        grid[lr][lc] = 0

    # 채우자
    for j in range(n):
        for i in range(n - 1, -1, -1):
            if grid[i][j] == 0:
                grid[i][j] = fill_lst.pop(0)

    while True:
        cnt = 0
        ele_location = []
        visited = [[False] * n for i in range(n)]
        for r in range(n):
            for c in range(n):
                if not visited[r][c]:
                    visited[r][c] = True
                    cnt += bfs(r, c)

        if cnt > 0:
            ans += len(ele_location)
            for lr, lc in ele_location:
                grid[lr][lc] = 0
            # 채우자
            for j in range(n):
                for i in range(n - 1, -1, -1):
                    if grid[i][j] == 0:
                        grid[i][j] = fill_lst.pop(0)
        else:
            break

    print(ans, end=" ")
