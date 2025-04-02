# 녹화본이 날라갔어요 ,,
n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

r, c = n // 2, n // 2
d = 0
two, num, cnt = 0, 1, 0
location = []
row_ = [0, 1, 0, -1]
col_ = [-1, 0, 1, 0]
while not (r == 0 and c == 0):
    location.append((r, c, d))
    r += row_[d]
    c += col_[d]

    cnt += 1
    if cnt == num:
        cnt = 0
        two += 1
        d = (d + 1) % 4
    if two == 2:
        num += 1
        two = 0
# 0123
# 좌하우상
dir_dict = {0: ((-1, 1, -2, 2, 0, -1, 1, -1, 1, 0),
                (1, 1, 0, 0, -2, 0, 0, -1, -1, -1)),
            1: ((-1, -1, 0, 0, 2, 0, 0, 1, 1, 1),
                (-1, 1, -2, 2, 0, -1, 1, -1, 1, 0)),
            2: ((-1, 1, -2, 2, 0, -1, 1, -1, 1, 0),
                (-1, -1, 0, 0, 2, 0, 0, 1, 1, 1)),
            3: ((1, 1, 0, 0, -2, 0, 0, -1, -1, -1),
                (-1, 1, -2, 2, 0, -1, 1, -1, 1, 0))
            }
percent = [(1, 0, 1), (2, 2, 3), (5, 4), (7, 5, 6), (10, 7, 8)]
ans = 0
for r, c, d in location:
    nr = r + row_[d]  # 다음 청소할 곳.
    nc = c + col_[d]
    munji = grid[nr][nc]
    grid[nr][nc] = 0  # 청소햇슈유..
    spread = 0
    for i in range(5):
        p, range_ = percent[i][0], percent[i][1:]
        for _ in range_:
            row, col = dir_dict[d][0][_], dir_dict[d][1][_]
            if not (0 <= nr + row < n and 0 <= nc + col < n):
                spread += (munji * p) // 100
                ans += (munji * p) // 100
            else:
                grid[nr + row][nc + col] += (munji * p) // 100
                spread += (munji * p) // 100
    a = munji - spread
    if (0 <= nr + dir_dict[d][0][9] < n and 0 <= nc + dir_dict[d][1][9] < n):
        grid[nr + dir_dict[d][0][9]][nc + dir_dict[d][1][9]] += a
    else:
        ans += a

print(ans)