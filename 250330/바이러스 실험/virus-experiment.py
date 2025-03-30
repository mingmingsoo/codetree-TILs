n, virus_num, time = map(int, input().split())
feed = [[5] * n for i in range(n)]
plus = [list(map(int, input().split())) for i in range(n)]  # 추가되는 양분
grid = [[[] for i in range(n)] for i in range(n)]
row = [-1, 1, 0, 0, 1, 1, -1, -1]
col = [0, 0, 1, -1, 1, -1, 1, -1]
for v in range(virus_num):
    r, c, age = map(int, input().split())
    grid[r - 1][c - 1].append(age)

for t in range(time):

    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                grid[i][j].sort()  # 오름차순 해주고
                die_idx = len(grid[i][j])
                for idx, age in enumerate(grid[i][j]):
                    if age <= feed[i][j]:
                        feed[i][j] -= age
                        grid[i][j][idx] += 1
                    else:
                        die_idx = idx
                        break

                for idx in range(die_idx, len(grid[i][j])):
                    feed[i][j] += grid[i][j][idx] // 2

                grid[i][j] = grid[i][j][:die_idx]
    # print("----양분----")
    # for _ in grid:
    #     print(_)
    # 번식
    for i in range(n):
        for j in range(n):
            for idx, age in enumerate(grid[i][j]):
                if age % 5 == 0:
                    for k in range(8):
                        nr = i + row[k]
                        nc = j + col[k]
                        if not (0 <= nr < n and 0 <= nc < n):
                            continue
                        grid[nr][nc].append(1)
    # print("----번식----")
    # for _ in grid:
    #     print(_)
    # 양분 추가
    for i in range(n):
        for j in range(n):
            feed[i][j] += plus[i][j]
    # print("----양분추가----")
    # for _ in feed:
    #     print(_)
ans = 0
for i in range(n):
    for j in range(n):
        ans += len(grid[i][j])
print(ans)
