'''
코드트리 2048게임
16:50 시작

문제설명
    두가지 동작
    1. 중력
    2. 합침
        단 합쳐질때 2 2 2 2가 있으면
        (2 2) (2 2) 이렇게 한번씩만 합쳐져서
        4 4 가 된다.
    5번 상하좌우 이동하여 얻을 수 있는 가장 큰 블록의 수

구상
    1. duple_perm : 방향의 순서를 정해주는 중복 순열
            00000도 가능
    2. game : 방향 순서대로 게임 시작
        - 중력
        - 합쳐
        - 중력
입력
    초기 상태 2048
출력
    게임 끝난 후 2048의 최댓값
'''

n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

sel = [0] * 5
ans = 0


def rotation(game_grid):
    grid = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            grid[i][j] = game_grid[n - j - 1][i]
    return grid


def gravity(game_grid):
    # 북쪽으로 땡긴당
    for j in range(n):
        while True:
            down = 0
            for i in range(n - 1):
                if game_grid[i][j] == 0 and game_grid[i + 1][j] != 0:
                    down += 1
                    game_grid[i][j], game_grid[i + 1][j] = game_grid[i + 1][j], game_grid[i][j]
            if not down:
                break


def merge(game_grid):
    # 북쪽으로 합친당
    for j in range(n):
        idx = 0
        while idx < n - 1:
            if game_grid[idx][j] and game_grid[idx][j] == game_grid[idx + 1][j]:
                game_grid[idx][j] *= 2
                game_grid[idx + 1][j] = 0
                idx += 1
            idx += 1


def duple_perm(idx):
    global ans, game_grid
    if idx == 5:
        # 여기서 게임진행
        game_grid = [_[:] for _ in grid]

        for d in sel:
            for ro in range(d):
                game_grid = rotation(game_grid)

            gravity(game_grid)
            merge(game_grid)
            gravity(game_grid)

        maxi = 0
        for i in range(n):
            for j in range(n):
                maxi = max(maxi, game_grid[i][j])
        ans = max(ans, maxi)

        return

    for i in range(4):
        sel[idx] = i
        duple_perm(idx + 1)


duple_perm(0)
print(ans)
