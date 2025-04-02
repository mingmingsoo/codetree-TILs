'''
실제 시험이다
문제 설명
    - 도넛
    1. 원자 이동 -> new_grid 필요
        방향 * 속력 만큼
    2. 2개 이상 있는 칸 뿜빠이
        [] 빈공간으로 만들어주고 대신
        add_lst에 넣어줌
    3. add_lst 추가.
헷갈리는게 뿜빠이 될때도 속력만큼?
'''

n, atom, time = map(int, input().split())
grid = [[[] for i in range(n)] for i in range(n)]
row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]
for a in range(atom):
    r, c, m, s, d = map(int, input().split())
    grid[r - 1][c - 1].append((m, s, d))

for t in range(time):
    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for m, s, d in grid[i][j]:
                    nr = (i + row[d] * s) % n
                    nc = (j + col[d] * s) % n
                    new_grid[nr][nc].append((m, s, d))

    # 상하좌우 0 2 4 6
    # 대각선   1 3 5 7
    add_lst = []
    for i in range(n):
        for j in range(n):
            if len(new_grid[i][j]) > 1:  # 찢어준다.
                l = len(new_grid[i][j])
                tm = ts = 0
                d_lst = []
                for m, s, d in new_grid[i][j]:
                    tm += m
                    ts += s
                    d_lst.append(d)
                new_grid[i][j] = []
                tm //= 5
                if tm == 0:
                    continue
                ts //= l
                udlr = 0
                for d in d_lst:
                    if d in (0, 2, 4, 6):
                        udlr += 1
                if udlr == 0 or udlr == l:
                    # 모두 상하좌우 혹은 모두 대각선
                    for d in (0, 2, 4, 6):
                        add_lst.append(((i + row[d] * ts) % n, (j + col[d] * ts) % n, tm, ts, d))
                else:
                    for d in (1,3,5,7):
                        add_lst.append(((i + row[d] * ts) % n, (j + col[d] * ts) % n, tm, ts, d))

    for r, c, m, s, d in add_lst:
        new_grid[r][c].append((m, s, d))
    grid = new_grid
ans = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            for m,s,d in grid[i][j]:
                ans += m

print(ans)