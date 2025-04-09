n, an, time = map(int, input().split())
grid = [[[] for i in range(n)] for i in range(n)]

for a in range(an):
    r, c, m, s, d = map(int, input().split())
    grid[r - 1][c - 1].append((m, s, d))

row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]

for t in range(time):
    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for atom in grid[i][j]:
                m, s, d = atom
                nr = (i + row[d] * s) % n
                nc = (j + col[d] * s) % n
                new_grid[nr][nc].append((m, s, d))

    for i in range(n):
        for j in range(n):
            if len(new_grid[i][j]) > 1:  # 합성 발생!!
                m_sm = 0
                s_sm = 0
                d_sm = 0
                cnt = len(new_grid[i][j])
                for m, s, d in new_grid[i][j]:
                    m_sm += m
                    s_sm += s
                    d_sm += d % 2

                nm = m_sm // 5
                new_grid[i][j] = []
                if nm == 0:
                    continue
                ns = s_sm // cnt
                if d_sm == 0 or d_sm == cnt:
                    for nd in (0, 2, 4, 6):
                        new_grid[i][j].append((nm, ns, nd))
                else:
                    for nd in (1, 3, 5, 7):
                        new_grid[i][j].append((nm, ns, nd))
    grid = new_grid

ans = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            for m, s, d in grid[i][j]:
                ans += m
print(ans)
