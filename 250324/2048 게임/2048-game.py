
n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

sel = [0] * 5
ans = 0


def rotation(game_grid):
    grid_copy = [_[:] for _ in game_grid]
    for i in range(n):
        for j in range(n):
            game_grid[i][j] = grid_copy[n - j - 1][i]


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
    global ans
    if idx == 5:
        # 여기서 게임진행
        game_grid = [_[:] for _ in grid]

        for d in sel:
            for ro in range(d):
                rotation(game_grid)

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
