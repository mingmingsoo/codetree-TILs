from collections import deque

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
arr = []
two = []
for i in range(n):
    for j in range(m):
        if grid[i][j] == 0:
            arr.append((i, j))
        elif grid[i][j] == 2:
            two.append((i, j))
sel = [0] * 3

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
ans = 0


def combi(sidx, idx):
    global ans
    if sidx == 3:
        grid_simul = [_[:] for _ in grid]
        q = deque(two)
        for r, c in sel:
            grid_simul[r][c] = 1
        while q:
            r, c = q.popleft()
            for k in range(4):
                nr = r + row[k]
                nc = c + col[k]
                if 0 <= nr < n and 0 <= nc < m and grid_simul[nr][nc] == 0:
                    grid_simul[nr][nc] = 2
                    q.append((nr, nc))
        sm = 0
        for i in range(n):
            for j in range(m):
                if grid_simul[i][j] == 0:
                    sm += 1
        ans = max(ans, sm)
        return

    if idx == len(arr):
        return

    sel[sidx] = arr[idx]
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


combi(0, 0)
print(ans)
