'''
문제설명
    4개의 말이 있을 때 받을 수 있는 최대 점수는?
구상
    1,2,3,4 중복순열
'''
cube = list(map(int, input().split()))  # 짬푸할 칸.
sel = [0] * 10
visited = [False] * 4
ans = 0
score = [[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40],
         [10, 13, 16, 19, 25, 30, 35, 40],
         [20, 22, 24, 25, 30, 35, 40],
         [30, 28, 27, 26, 25, 30, 35, 40]]


def perm(idx):
    global ans
    if idx == 10:
        ele_score = 0
        state = [(0, -1) for i in range(4)]
        end = [False] * 4
        for i in range(10):
            horse = sel[i] - 1
            dice = cube[i]
            if end[horse]:
                continue

            nr, nc = state[horse][0], state[horse][1] + dice

            if (nr, nc) == (0, 4):  # 10
                (nr, nc) = (1, 0)  # 위치 바꿔줌
            elif (nr, nc) == (0, 9):  # 20
                (nr, nc)= (2, 0)
            elif (nr, nc) == (0, 14):  # 30
                (nr, nc) = (3, 0)
            elif (nr, nc) == (0, 19) or (nr, nc) == (1, 7) or (nr, nc) == (2, 6):  # 40
                (nr, nc) = (3, 7)

            if nr == 0 and nc > 19:
                end[horse] = True
                continue
            elif nr == 1 and nc > 7:
                end[horse] = True
                continue
            elif nr == 2 and nc > 6:
                end[horse] = True
                continue
            elif nr == 3 and nc > 7:
                end[horse] = True
                continue

            go = True
            for j in range(4):
                if j == horse:
                    continue
                hr, hc = state[j]
                if (hr, hc) == (nr, nc):
                    go = False
                    break
            if go:
                state[horse] = (nr, nc)
                ele_score += score[nr][nc]

        ans = max(ans, ele_score)
        return
    for i in range(1, 5):
        sel[idx] = i
        perm(idx + 1)


perm(0)
print(ans)
