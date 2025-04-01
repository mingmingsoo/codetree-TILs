'''
손코딩 X 문제 설명 그대로...
입력
    맵크기 n, 원자 갯수 m, 실험시간 k
    원자 정보 r,c,m,s,d
출력
    k초 후 남아있는 원자 질량 합
'''

n, player_num, time = map(int, input().split())
grid = [[[] for i in range(n)] for i in range(n)]
for p in range(player_num):
    r, c, m, s, d = map(int, input().split())
    grid[r - 1][c - 1].append((m, s, d))


row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]
for t in range(time):
    new_grid = [[[] for i in range(n)] for i in range(n)]
    # 1. 이동
    for i in range(n):
        for j in range(n):
            for m, s, d in grid[i][j]:
                nr = (i + row[d] * s) % n
                nc = (j + col[d] * s) % n
                new_grid[nr][nc].append((m, s, d))

    # 2. 이동이 끝난 뒤 2개이상 원자는 합성
    new_grid2 = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if len(new_grid[i][j]) > 1:
                length = len(new_grid[i][j])
                tm = 0
                ts = 0
                dlst = []
                for m, s, d in new_grid[i][j]:
                    tm += m
                    ts += s
                    dlst.append(d)
                nm = tm // 5
                ns = ts // length
                new_grid[i][j] = []
                if nm == 0:
                    continue
                # 모두 상하좌우 or 모두 대각선 -> 상하좌우
                udlr = 0
                for dd in dlst:
                    if dd in (0, 2, 4, 6):
                        udlr += 1
                if udlr == 0 or udlr == length:
                    for k in (0, 2, 4, 6):
                        nr = (i + row[k]*ns) % n
                        nc = (j + col[k]*ns) % n
                        new_grid2[nr][nc].append((nm, ns, k))
                else:
                    for k in (1, 3, 5, 7):
                        nr = (i + row[k]*ns) % n
                        nc = (j + col[k]*ns) % n
                        new_grid2[nr][nc].append((nm, ns, k))
            elif new_grid[i][j]:
                m,s,d = new_grid[i][j][0]
                new_grid2[i][j].append((m,s,d))



    grid = new_grid2

ans = 0
for i in range(n):
    for j in range(n):
       if grid[i][j]:
           for m,s,d in grid[i][j]:
               ans += m
print(ans)