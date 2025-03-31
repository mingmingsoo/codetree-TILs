n, player_num, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
area = [[0] * n for i in range(n)]
tmp = list(map(int, input().split()))
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            grid[i][j] = [grid[i][j], tmp[grid[i][j] - 1] - 1]
pq = []
for p in range(player_num):
    pq_tmp = [list(map(lambda x: int(x) - 1, input().split())) for i in range(4)]
    pq.append(pq_tmp)


def end():
    for i in range(n):
        for j in range(n):
            if grid[i][j] and grid[i][j][0] > 1:
                return False
    return True


row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]
ans = -1
for t in range(1, 1000):
    # 냄새 남기기
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                area[i][j] = [grid[i][j][0], time]

    visited = [False] * (player_num + 1)
    # 이동하기.
    for i in range(n):
        for j in range(n):
            if grid[i][j] and not visited[grid[i][j][0]]:
                visited[grid[i][j][0]] = True
                empty = False
                next_r, next_c, next_d = i, j, grid[i][j][1]
                for k in pq[grid[i][j][0] - 1][grid[i][j][1]]:
                    nr = i + row[k]
                    nc = j + col[k]
                    if 0 <= nr < n and 0 <= nc < n and area[nr][nc] == 0:
                        empty = True
                        next_r, next_c, next_d = nr, nc, k
                        break
                if not empty:
                    for k in pq[grid[i][j][0] - 1][grid[i][j][1]]:
                        nr = i + row[k]
                        nc = j + col[k]
                        if 0 <= nr < n and 0 <= nc < n and area[nr][nc][0] == grid[i][j][0]:
                            next_r, next_c, next_d = nr, nc, k
                            break
                grid[i][j][1] = next_d
                if grid[next_r][next_c] == 0:
                    grid[next_r][next_c], grid[i][j] = grid[i][j], grid[next_r][next_c]
                else:
                    if grid[next_r][next_c][0] > grid[i][j][0]:
                        grid[next_r][next_c] = grid[i][j]
                        grid[i][j] = 0
                    else:
                        grid[i][j] = 0  # die

    if end():
        ans = t
        break

    # 냄새 빼주기
    for i in range(n):
        for j in range(n):
            if area[i][j]:
                area[i][j][1] -= 1
                if area[i][j][1] <= 0:
                    area[i][j] = 0

print(ans)
