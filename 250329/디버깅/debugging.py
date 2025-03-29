m, origin_num, n = map(int, input().split())
m = 2 * m - 1
grid = [[0] * (m) for i in range(n)]

for i in range(n):
    for j in range(0, m, 2):
        grid[i][j] = 1

for o in range(origin_num):
    r, c = map(int, input().split())
    grid[r - 1][2 * c - 1] = 1
arr = []
for i in range(n):
    for j in range(m):
        if not grid[i][j]:
            arr.append((i, j))


find = False


def is_ok():
    for j in range(0, m, 2):
        r, c = 0, j
        while r < n:
            left = False
            while c > 0 and grid[r][c - 1]:
                left = True
                c -= 1
            while not left and c < m - 1 and grid[r][c + 1]:
                c += 1
            r += 1
        if c != j:
            return False
    return True


def combi(sidx, idx):
    global find, grid
    if find:
        return
    if sidx == i:
        grid_origin = [_[:] for _ in grid]
        for r, c in sel:
            grid[r][c] = 1

        if is_ok():
            find = True
            return

        grid = [_[:] for _ in grid_origin]
        return
    if idx == len(arr):
        return

    if sidx > 0:
        nr, nc = arr[idx]  # 내가 선택할 것
        r, c = sel[sidx - 1]  # 내가 전에 선택한 것.
        if (r == nr) and (nc - c) == 2:  # 가로 연결되면 다음 거
            combi(sidx, idx + 1)
            return

    sel[sidx] = arr[idx]
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


ans = -1
for i in range(0, 4):
    sel = [0] * i
    combi(0, 0)
    if find:
        ans = i
        break
print(ans)
