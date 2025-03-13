'''
문제설명
    승용이가 0~ C-1 까지 가는데 채취한 곰팡이 총 합
구상
    1. 승용이 움직임
    2. 승용이 채취함
    3. 이동함
    4. 합쳐짐
    속도는 2(크기 -1) 로 나눠줌
    와리가리는 2(크기-1)임
5 6 1
3 3 999 4 1

5 6 1
3 3 998 4 1

'''

n, m, virus_num = map(int, input().split())  # 맵 크기와 곰팡이 수
grid = [[[] for i in range(m)] for i in range(n)]
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
for v in range(virus_num):
    r, c, s, d, b = map(int, input().split())  # 위치, 속력, 방향, 크기
    if d in (1, 2):  # 위 아래
        grid[r - 1][c - 1].append((b, d - 1, s % (2 * (n - 1))))  # 크기, 방향, 속력 순으로 넣는다
    else:
        grid[r - 1][c - 1].append((b, d - 1, s % (2 * (m - 1))))

move = {0: 1, 1: 0, 2: 3, 3: 2}
jdx = 0
eat = 0
while jdx < m:  # 승용이 움직임
    # print("--------이동전!-----------")
    # for i in range(n):
    #     for j in range(m):
    #         if grid[i][j]:
    #             print(grid[i][j][0][0], end=" ")
    #         else:
    #             print(0, end=" ")
    #     print()
    # 1. 누구 먹을래
    for i in range(n):
        if grid[i][jdx]:  # 곰팡이 있으면
            eat += grid[i][jdx][0][0]  # 크기만큼 먹는다
            grid[i][jdx] = []  # 비었다!
            break
    # 2. 움직인다.
    new_grid = [[[] for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                for w in range(len(grid[i][j]) - 1, -1, -1):
                    virus = grid[i][j][w]
                    b, d, s = virus[0], virus[1], virus[2]  # 크기, 방향, 속력
                    nr = i + row[d] * s
                    nc = j + col[d] * s
                    if d in (0, 1):
                        size = 2 * (n - 1)
                        nr = (nr + size) % size
                        if nr >= n:
                            nr = size - nr
                            d = move[d]
                    elif d in (2, 3):
                        size = 2 * (m - 1)
                        nc = (nc + size) % size
                        if nc >= m:
                            nc = size - nc
                            d = move[d]
                    new_grid[nr][nc].append((b, d, s))
                    # grid[i][j].pop(w)
    # 3-0. sort 하고
    for i in range(n):
        for j in range(m):
            if new_grid[i][j]:
                new_grid[i][j].sort(reverse=True)
    # 3-1. 겹치는 애들 검사
    for i in range(n):
        for j in range(m):
            if len(new_grid[i][j]) >= 2:
                new_grid[i][j] = [new_grid[i][j][0]]
    grid = new_grid
    jdx += 1  # 다음 칸 탐색
    # print("--------이동후!-----------")
    # for i in range(n):
    #     for j in range(m):
    #         if grid[i][j]:
    #             print(grid[i][j][0][0], end=" ")
    #         else:
    #             print(0, end=" ")
    #     print()
print(eat)
