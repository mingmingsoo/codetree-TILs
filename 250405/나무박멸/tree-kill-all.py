'''
문제 설명
    1. 나무 성장
    2. 나무 번식 - plus_grid 필요
    3. 제초제 - 조건 확인 -> 정답 더해주기
        - c+1년 제초제 남기기 -> kill_grid 필요
        - -1년 빼주기
입력
    맵 n, 총 년 수 turn, 확산 범위 l, 제초제 년수 kill

5 5 2 1
0 0 0 0 0
0 30 23 0 0
0 0 -1 0 0
0 0 17 46 77
0 0 0 12 0

5 5 2 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0

5 5 2 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
'''

n, turn, length, kill = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
kill_grid = [[0] * n for i in range(n)]
ans = 0
row = [-1, 1, 0, 0, 1, 1, -1, -1]
col = [0, 0, 1, -1, 1, -1, 1, -1]
for t in range(turn):

    # 1. 나무 성장
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                cnt = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 0:
                        cnt += 1
                grid[i][j] += cnt

    # 2. 번식
    plus_grid = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                cnt = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and kill_grid[nr][nc] == 0:
                        cnt += 1
                if cnt:
                    tree = grid[i][j] // cnt
                    for k in range(4):
                        nr = i + row[k]
                        nc = j + col[k]
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and kill_grid[nr][nc] == 0:
                            plus_grid[nr][nc] += tree
    for i in range(n):
        for j in range(n):
            if plus_grid[i][j]:
                grid[i][j] += plus_grid[i][j]

    # 3. 제초제
    lst = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                sm = grid[i][j]
                for k in range(4, 8):
                    for l in range(1, length + 1):
                        nr = i + row[k] * l
                        nc = j + col[k] * l
                        if not (0 <= nr < n and 0 <= nc < n):
                            break
                        if grid[nr][nc] > 0:
                            sm += grid[nr][nc]
                        else:
                            break
                lst.append((-sm, (i, j)))
    if lst:
        lst.sort()
        tree, (r, c) = lst[0]
        ans += abs(tree)

        # 제초제 뿌리고 년 수 기록
        for k in range(4, 8):
            for l in range(1, length + 1):
                nr = r + row[k] * l
                nc = c + col[k] * l
                if not (0 <= nr < n and 0 <= nc < n):
                    break
                if grid[nr][nc] > 0:
                    grid[nr][nc] = 0
                    kill_grid[nr][nc] = kill + 1
                else:
                    kill_grid[nr][nc] = kill + 1
                    break
        grid[r][c] = 0
        kill_grid[r][c] = kill + 1  # 본인 위치도

    for i in range(n):
        for j in range(n):
            if kill_grid[i][j]:
                kill_grid[i][j] -= 1

print(ans)
