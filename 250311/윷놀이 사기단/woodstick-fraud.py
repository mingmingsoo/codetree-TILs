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
        state = [(-1, -1) for i in range(4)]
        end = [False] * 4
        for i in range(10):
            horse = sel[i] - 1
            dice = cube[i]
            if end[horse]:
                continue
            if state[horse] == (-1, -1):  # 시작도 안했으면?
                go = True
                for hr, hc in state:
                    if (hr, hc) == (0, dice - 1):
                        go = False
                        break
                if go:
                    state[horse] = (0, dice - 1)  # 일단 옮겨준다.
                    ele_score += score[0][dice - 1]
                else:
                    continue
            elif state[horse][0] == 0 and state[horse][1] + dice > 19:
                end[horse] = True
                continue
            elif state[horse][0] == 1 and state[horse][1] + dice > 7:
                end[horse] = True
                continue
            elif state[horse][0] == 2 and state[horse][1] + dice > 6:
                end[horse] = True
                continue
            elif state[horse][0] == 3 and state[horse][1] + dice > 7:
                end[horse] = True
                continue
            else:  # 그게 아니라면
                go = True
                for hr, hc in state:
                    if (hr, hc) == (state[horse][0], state[horse][1] + dice):
                        go = False
                        break
                if go:
                    origin_r, origin_c = (state[horse][0], state[horse][1])
                    state[horse] = (state[horse][0], state[horse][1] + dice)  # 옮겨준다.
                    if (state[horse][0], state[horse][1]) == (0, 4):  # 10
                        state[horse] = (1, 0)  # 위치 바꿔줌
                    elif (state[horse][0], state[horse][1]) == (0, 9):  # 20
                        state[horse] = (2, 0)
                    elif (state[horse][0], state[horse][1]) == (0, 14):  # 30
                        state[horse] = (3, 0)
                    elif (state[horse][0], state[horse][1]) == (0, 19) or (state[horse][0], state[horse][1]) == (
                    1, 7) or (state[horse][0], state[horse][1]) == (2, 6):  # 40
                        state[horse] = (3, 7)
                    go = True
                    for i in range(4):
                        if i == horse:
                            continue
                        hr, hc = state[i]
                        if (hr, hc) == (state[horse][0], state[horse][1]):
                            go = False
                            state[horse]= ( origin_r, origin_c)
                            break
                    if go:
                        ele_score += score[state[horse][0]][state[horse][1]]
                else:
                    continue
            if (state[horse][0], state[horse][1]) == (0, 4):  # 10
                state[horse] = (1, 0)  # 위치 바꿔줌
            elif (state[horse][0], state[horse][1]) == (0, 9):  # 20
                state[horse] = (2, 0)
            elif (state[horse][0], state[horse][1]) == (0, 14):  # 30
                state[horse] = (3, 0)
            elif (state[horse][0], state[horse][1]) == (0, 19) or (state[horse][0], state[horse][1]) == (1, 7) or (state[horse][0], state[horse][1]) == (2, 6):  # 40
                state[horse] = (3, 7)
        ans = max(ans, ele_score)
        return
    for i in range(1, 5):
        sel[idx] = i
        perm(idx + 1)


perm(0)
print(ans)
