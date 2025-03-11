'''
틀린이유
    .... 가려는 위치에 말이 있으면 말이 대기하는 건 줄 알았ㅇㅁ..............
    .....ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ
    ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ
    ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ
    ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ

문제설명
    4개의 말이 있을 때 받을 수 있는 최대 점수는?

구상
    1,2,3,4 중복순열

반례
5 5 5 5 5 5 5 5 5 5
정답 130


'''
'''
문제설명
    4개의 말이 있을 때 받을 수 있는 최대 점수는?
구상
    1,2,3,4 중복순열
반례
5 5 5 5 5 5 5 5 5 5
정답 130

25 처리해주는 게 필요함.
'''
cube = list(map(int, input().split()))  # 짬푸할 칸.
sel = [0] * 10
ans = 0
score = [[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40],
         [10, 13, 16, 19, 25],
         [20, 22, 24, 25],
         [30, 28, 27, 26, 25],
         [25, 30, 35, 40]]


def perm(idx):
    global ans
    if idx == 10:
        ele_score = 0
        state = [(0, -1) for i in range(4)]
        for i in range(10):
            if (10 - i) * 40 + ele_score < ans:
                return
            horse = sel[i] - 1
            dice = cube[i]
            if (state[horse][0], state[horse][1]) == (-1, -1):
                return
            nr, nc = state[horse][0], state[horse][1] + dice

            if (nr, nc) == (0, 4):  # 10
                (nr, nc) = (1, 0)  # 위치 바꿔줌
            elif (nr, nc) == (0, 9):  # 20
                (nr, nc) = (2, 0)
            elif (nr, nc) == (0, 14):  # 30
                (nr, nc) = (3, 0)
            elif (nr, nc) == (0, 19):  # 40
                (nr, nc) = (3, 7)
            if 0 < nr < 4 and nc >= len(score[nr]) - 1:
                nc = nc - len(score[nr]) + 1
                nr = 4

            if nr == 0 and nc > 19:
                state[horse] = (-1, -1)
                continue
            elif nr == 4 and nc > 3:
                state[horse] = (-1, -1)
                continue

            for j in range(4):
                if j == horse:
                    continue
                hr, hc = state[j]
                if (hr, hc) == (nr, nc):
                    return
            state[horse] = (nr, nc)
            ele_score += score[nr][nc]
        ans = max(ans, ele_score)
        return
    for i in range(1, 5):
        sel[idx] = i
        perm(idx + 1)


perm(0)
print(ans)
