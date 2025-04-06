'''
문제 설명
    1. 참가자 이동
    2. 미로 회전
입력
    맵 크기 n, 참가자 수 m, 게임시간 k
    맵 정보 (1~9 벽)
    참가자 좌표
    출구좌표
출력
    참가자 이동거리합, 출구좌표
필요한 함수
    move()
    rotation() - 브루트포스, 회전 필요
필요한 변수
    grid - 벽 좌표, 탈출구 -1 처리
    player_grid - 3차원, 플레이어 맵

5 3 20
0 0 0 0 1
9 2 2 0 0
0 1 0 1 0
0 0 0 1 0
0 0 0 0 0
1 3
3 1
3 5
3 3

5 2 2
0 0 0 0 0
0 0 0 0 0
0 1 0 0 0
0 0 0 0 0
0 0 0 0 0
1 2
2 2
4 2
'''
n, pn, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
player_grid = [[[] for i in range(n)] for i in range(n)]
for p in range(pn):
    r, c = map(lambda x: int(x) - 1, input().split())
    player_grid[r][c].append(p + 1)
er, ec = map(lambda x: int(x) - 1, input().split())
grid[er][ec] = -1
total_move = 0

row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]

exit_num = 0


def move():
    global total_move, player_grid, exit_num
    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if player_grid[i][j]:
                for p in player_grid[i][j]:
                    move = False
                    cur = abs(i - er) + abs(j - ec)
                    for k in range(4):
                        nr = i + row[k]
                        nc = j + col[k]
                        if not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc] > 0:
                            continue
                        next = abs(nr - er) + abs(nc - ec)
                        if next < cur:
                            if (nr, nc) != (er, ec):
                                new_grid[nr][nc].append(p)
                            else:
                                exit_num += 1
                            move = True
                            total_move += 1
                            break
                    if not move:
                        new_grid[i][j].append(p)
    player_grid = new_grid
    # print("이동 후")
    # for _ in player_grid:
    #     print(_)


def rotation():
    global er,ec
    L, R, C = 0, 0, 0
    for l in range(2, n + 1):
        for r in range(0, n - l + 1):
            for c in range(0, n - l + 1):
                is_exit = is_people = False
                for i in range(r, r + l):
                    for j in range(c, c + l):
                        if player_grid[i][j]:
                            is_people = True
                        if grid[i][j] == -1:
                            is_exit = True
                if is_exit and is_people:
                    L, R, C = l, r, c
                    break
            if L:
                break
        if L:
            break

    # print("선택한 사각형:", L, R, C)
    small_grid = [_[C:C + L] for _ in grid[R:R + L]]
    small_player_grid = [[__[:] for __ in _[C:C + L]] for _ in player_grid[R:R + L]]

    small_ro_grid = [[0] * L for i in range(L)]
    small_ro_player_grid = [[[] for i in range(L)] for i in range(L)]

    for i in range(L):
        for j in range(L):
            small_ro_grid[i][j] = small_grid[L - j - 1][i]
            if small_ro_grid[i][j] > 0:
                small_ro_grid[i][j] -= 1
            small_ro_player_grid[i][j] = small_player_grid[L - j - 1][i][:]
    # print("----------")
    # for _ in small_ro_grid:
    #     print(_)
    #
    # print("----------")
    # for _ in small_ro_player_grid:
    #     print(_)

    for i in range(L):
        for j in range(L):
            grid[i + R][j + C] = small_ro_grid[i][j]
            if grid[i + R][j + C] == -1:
                er, ec = i + R, j + C
            player_grid[i + R][j + C] = small_ro_player_grid[i][j][:]

    # print("----회전후------")
    # for _ in grid:
    #     print(_)
    #
    # print("----------")
    # for _ in player_grid:
    #     print(_)

for t in range(time):
    # print("-------",t,"------------")
    move()

    if exit_num == pn:
        break
    rotation()

print(total_move)
print(er+1,ec+1)