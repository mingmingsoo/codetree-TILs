block_num = int(input())
m, n = 4, 6
yel = [[0] * m for i in range(n)]
red = [[0] * m for i in range(n)]
sc = 0


def location():
    if shape == 1:
        # 그냥 네모
        nr = n - 1
        for i in range(n):
            if yel[i][c]:
                nr = i - 1
                break
        yel[nr][c] = 1

        nr = n - 1
        for i in range(n):
            if red[i][3 - r]:
                nr = i - 1
                break
        red[nr][3 - r] = 1

    elif shape == 2:
        # 가로
        nr = n - 1
        for i in range(n):
            if yel[i][c] or yel[i][c + 1]:
                nr = i - 1
                break
        yel[nr][c] = yel[nr][c + 1] = 1

        nr = n - 1
        for i in range(n):
            if red[i][3 - r]:
                nr = i - 1
                break
        red[nr][3 - r] = red[nr - 1][3 - r] = 1

    elif shape == 3:
        # 세로
        nr = n - 1
        for i in range(n):
            if yel[i][c]:
                nr = i - 1
                break
        yel[nr][c] = yel[nr - 1][c] = 1

        nr = n - 1
        for i in range(n):
            if red[i][3 - r] or red[i][3 - r - 1]:
                nr = i - 1
                break
        red[nr][3 - r] = red[nr][3 - r - 1] = 1


def delete(grid):
    global sc
    for i in range(n - 1, -1, -1):
        if grid[i].count(1) == 4:
            sc += 1
            grid.pop(i)
            grid.insert(0, [0] * 4)


def special(grid):
    cnt = 0
    for i in range(2):
        if 1 in grid[i]:
            cnt += 1
    for _ in range(cnt):
        grid.pop()
        grid.insert(0, [0] * 4)


for b in range(block_num):
    shape, r, c = map(int, input().split())
    location()  # 위치시키기
    # print("----yellow----")
    # for _ in yel:
    #     print(_)
    # print("----red----")
    # for _ in red:
    #     print(_)
    delete(yel)  # 한 줄 채워진 애들 지우기 + 점수
    delete(red)
    # print("----yellow 한 줄 지워----")
    # for _ in yel:
    #     print(_)
    # print("----red 한 줄 지워----")
    # for _ in red:
    #     print(_)
    special(yel)
    special(red)
    # print("----yellow 스페샬----")
    # for _ in yel:
    #     print(_)
    # print("----red 스페샬----")
    # for _ in red:
    #     print(_)

print(sc)
print(sum(map(sum, red)) + sum(map(sum, yel)))