'''
말들을 모두 arr 에 담고
idx 로 모든 경우의 수를 탐색
출력은 전체 맵 크기 - 갈수 있는 체스판의 최댓값
'''

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

arr = []
visited = [[0] * m for i in range(n)]
for i in range(n):
    for j in range(m):
        if 0 < grid[i][j] < 6:
            arr.append((i, j, grid[i][j]))
        elif grid[i][j] == 6:
            visited[i][j] = 1

ans = 0


def left(r, c, visited):
    for j in range(c, -1, -1):
        if grid[r][j] == 6:
            break
        visited[r][j] = 1

def right(r, c, visited):
    for j in range(c, m):
        if grid[r][j] == 6:
            break
        visited[r][j] = 1


def up(r, c, visited):
    for i in range(r, -1, -1):
        if grid[i][c]== 6:
            break
        visited[i][c] = 1


def down(r, c, visited):
    for i in range(r, n):
        if grid[i][c]== 6:
            break
        visited[i][c] = 1


def btk(idx):
    global ans, visited
    if idx == len(arr):
        sm = sum(map(sum, visited))
        ans = max(ans, sm)
        return

    r, c, shape = arr[idx]
    visited_copy = [_[:] for _ in visited]
    if shape == 1:
        left(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        right(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        up(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        down(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

    elif shape == 2:
        left(r, c, visited)
        right(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        up(r, c, visited)
        down(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

    elif shape == 3:
        up(r, c, visited)
        right(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        right(r, c, visited)
        down(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        down(r, c, visited)
        left(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        left(r, c, visited)
        up(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

    elif shape == 4:
        up(r, c, visited)
        right(r, c, visited)
        down(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        right(r, c, visited)
        down(r, c, visited)
        left(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        down(r, c, visited)
        left(r, c, visited)
        up(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

        left(r, c, visited)
        up(r, c, visited)
        right(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]

    elif shape == 5:
        left(r, c, visited)
        right(r, c, visited)
        up(r, c, visited)
        down(r, c, visited)
        btk(idx + 1)
        visited = [_[:] for _ in visited_copy]


btk(0)
print(n * m - ans)
