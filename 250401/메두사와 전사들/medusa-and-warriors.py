'''
옝니 코드 디버깅
'''
di, dj = [-1, -1, 0, 1, 1, 1, 0, -1], [0, 1, 1, 1, 0, -1, -1, -1]   # 12시 방향부터 0, 시계 방향 순서대로 1씩 증가
N, M = map(int, input().split())
warriors = [[]]                                                 # 전사 위치 좌표 관리
field = [[[] for _ in range(N)] for _ in range(N)]              # 전사 위치 표시
rocks = [0 for _ in range(M+1)]                                 # 현재 돌 됐는지 여부를 관리할 배열
mi, mj, er, ec = map(int, input().split())

lst = list(map(int, input().split()))

idx = 1
for i in range(0, len(lst)-1, 2):
    warriors.append([lst[i], lst[i+1]])
    field[lst[i]][lst[i+1]].append(idx)
    idx += 1

arr = [list(map(int, input().split())) for _ in range(N)]       # 도로 정보 & 공원 표시
arr[er][ec] = 'P'

def oob(ti, tj):
    return not (0<=ti<N and 0<=tj<N)

def distance(ai, aj, bi, bj):
    return abs(ai-bi) + abs(aj-bj)

# 메두사 이동 함수
def move_medusa():

    q = [[mi, mj]]
    v = [[[] for _ in range(N)] for _ in range(N)]
    v[mi][mj].append([mi, mj])
    path = []

    while q:
        tmp = q
        q = []

        for t in tmp:
            if arr[t[0]][t[1]] == 'P':
                path = v[t[0]][t[1]]
                break

            for x in (0, 4, 6, 2):
                ni, nj = t[0] + di[x], t[1] + dj[x]

                # 범위내, 미방문, 도로(0)
                if not oob(ni, nj) and not v[ni][nj] and arr[ni][nj] != 1:
                    q.append([ni, nj])
                    v[ni][nj] = v[t[0]][t[1]] + [[ni, nj]]

        if path:
            break

    # 공원에 도달하지 못했다면 빈 배열 반환
    if not path:
        return [-1, -1]

    return path[1]

# 초기 시야각 배열 만드는 함수
def make_view(direction):

    # 위쪽 시야각
    tmp_view = [[0 for _ in range(N)] for _ in range(N)]
    if direction == 0:
        start, can_see = mi-1, 1

        while start >= 0:
            for j in range(mj - can_see, mj + can_see + 1):
                if oob(start, j): continue

                tmp_view[start][j] = 1
            start -= 1
            can_see += 1

    elif direction == 4:
        start, can_see = mi + 1, 1

        while start < N:
            for j in range(mj - can_see, mj + can_see + 1):
                if oob(start, j): continue

                tmp_view[start][j] = 1
            start += 1
            can_see += 1

    elif direction == 6:
        start, can_see = mj - 1, 1

        while start >= 0:
            for i in range(mi - can_see, mi + can_see + 1):
                if oob(i, start): continue
                tmp_view[i][start] = 1
            start -= 1
            can_see += 1

    else:
        start, can_see = mj + 1, 1

        while start < N:
            for i in range(mi - can_see, mi + can_see + 1):
                if oob(i, start): continue
                tmp_view[i][start] = 1
            start += 1
            can_see += 1

    return tmp_view

# 전사 - 메두사 상대 위치 파악 (시야각 없어지는 방향 반환)
def get_relative_pos(ci, cj, d):

    if d == 0:
        if cj < mj:return [0, 7]
        elif cj == mj:
            return [0]
        else:return [0, 1]
    elif d == 4:
        if cj < mj:return [4, 5]
        elif cj == mj:
            return [4]
        else:return [3, 4]
    elif d == 6:
        if ci < mi:return [6, 7]
        elif ci == mi:
            return [6]
        else:return [5, 6]
    else:
        if ci < mi:return [1, 2]
        elif ci == mi:
            return [2]
        else:return [2, 3]

# 시야각 재조정
def rearrange_view(ci, cj, cview, direcs):

    if len(direcs) == 1:
        move = 1
        while True:
            ni, nj = ci + move * di[direcs[0]], cj + move * dj[direcs[0]]

            if oob(ni, nj): break
            cview[ni][nj] = 0
            move += 1
    else:
        if direcs == [0, 7]:
            cnt = 2
            for ii in range(ci - 1, -1, -1):
                for jj in range(cj, cj - cnt, -1):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [0, 1]:
            cnt = 2
            for ii in range(ci - 1, -1, -1):
                for jj in range(cj, cj + cnt):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [4, 5]:
            cnt = 2
            for ii in range(ci + 1, N):
                for jj in range(cj, cj - cnt, -1):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [3, 4]:
            cnt = 2
            for ii in range(ci + 1, N):
                for jj in range(cj, cj + cnt):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [6, 7]:
            cnt = 2
            for jj in range(cj - 1, -1, -1):
                for ii in range(ci, ci - cnt, -1):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [5, 6]:
            cnt = 2
            for jj in range(cj - 1, -1, -1):
                for ii in range(ci, ci + cnt):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [1, 2]:
            cnt = 2
            for jj in range(cj + 1, N):
                for ii in range(ci, ci - cnt, -1):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1
        elif direcs == [2, 3]:
            cnt = 2
            for jj in range(cj + 1, N):
                for ii in range(ci, ci + cnt):
                    if oob(ii, jj): break
                    cview[ii][jj] = 0
                cnt += 1

# 시선에 들어오는 전사들 확인
def check_seesun(cview, direction):

    sm = 0                                                          # 돌로 변한 전사 수
    tmp_rocks = []
    if direction == 0:
        for i in range(mi - 1, -1, -1):
            for j in range(N):

                if cview[i][j] == 0:                                # 시야각에 들어오지 않는 칸은 생략
                    continue

                if field[i][j]:
                    sm += len(field[i][j])
                    for warr in field[i][j]:                        # 돌로 변하는 전사 번호 저장
                        tmp_rocks.append(warr)
                    direcs = get_relative_pos(i, j, direction)      # 전사에 의해 가려지는 방향
                    rearrange_view(i, j, cview, direcs)

    elif direction == 4:
        for i in range(mi + 1, N):
            for j in range(N):
                if cview[i][j] == 0:                                # 시야각에 들어오지 않는 칸은 생략
                    continue

                if field[i][j]:
                    sm += len(field[i][j])
                    for warr in field[i][j]:                        # 돌로 변하는 전사 번호 저장
                        tmp_rocks.append(warr)
                    direcs = get_relative_pos(i, j, direction)      # 전사에 의해 가려지는 방향
                    rearrange_view(i, j, cview, direcs)

    elif direction == 6:
        for j in range(mj - 1, -1, -1):
            for i in range(N):
                if cview[i][j] == 0:                                # 시야각에 들어오지 않는 칸은 생략
                    continue

                if field[i][j]:
                    sm += len(field[i][j])
                    for warr in field[i][j]:                        # 돌로 변하는 전사 번호 저장
                        tmp_rocks.append(warr)
                    direcs = get_relative_pos(i, j, direction)      # 전사에 의해 가려지는 방향
                    rearrange_view(i, j, cview, direcs)

    else:
        for j in range(mj + 1, N):
            for i in range(N):
                if cview[i][j] == 0:                                # 시야각에 들어오지 않는 칸은 생략
                    continue

                if field[i][j]:
                    sm += len(field[i][j])
                    for warr in field[i][j]:                        # 돌로 변하는 전사 번호 저장
                        tmp_rocks.append(warr)
                    direcs = get_relative_pos(i, j, direction)      # 전사에 의해 가려지는 방향
                    rearrange_view(i, j, cview, direcs)

    return sm, tmp_rocks, cview

# 메두사 시선
def seesun_medusa():
    global rocks

    turn_rocks = []                                             # 돌로 변할 전사 인덱스 리스트
    mx = 0
    ret_view = []
    for x in (0, 4, 6, 2):
        view = make_view(x)                                     # 방향에 따른 시야각 생성
        turn_rock_cnt, tmp_rocks, view = check_seesun(view, x)        # 방향별로 시야에 들어오는 전사 수
        if mx < turn_rock_cnt:
            ret_view = view
            turn_rocks = tmp_rocks
            mx = turn_rock_cnt

    for t in turn_rocks:
        rocks[t] = 1

    return ret_view


# 전사 이동
def move_warriors():

    sm = 0                                              # 전사들 이동 칸 수
    attack = 0
    for i in range(1, M+1):
        if not warriors[i] or rocks[i] == 1:
            continue

        # 첫 번째 이동
        wi, wj = warriors[i]
        dist = distance(wi, wj, mi, mj)
        for x in (0, 4, 6, 2):
            ni, nj = wi + di[x], wj + dj[x]

            if not oob(ni, nj) and distance(ni, nj, mi, mj) < dist and view[ni][nj] == 0:
                field[ni][nj].append(field[wi][wj].pop(field[wi][wj].index(i)))
                sm += 1
                wi, wj = ni, nj
                dist = distance(ni, nj, mi, mj)
                break

        # 메두사와 같은 칸에 도달했을 경우 주금
        if [wi, wj] == [mi, mj]:
            attack += 1
            field[wi][wj].pop(field[wi][wj].index(i))
            warriors[i] = []
            continue

        # 두 번째 이동
        for x in (6, 2, 0, 4):
            ni, nj = wi + di[x], wj + dj[x]

            if not oob(ni, nj) and distance(ni, nj, mi, mj) < dist and view[ni][nj] == 0:
                field[ni][nj].append(field[wi][wj].pop(field[wi][wj].index(i)))
                sm += 1
                wi, wj = ni, nj
                break

        # 메두사와 같은 칸에 도달했을 경우 주금
        if [wi, wj] == [mi, mj]:
            attack += 1
            field[wi][wj].pop(field[wi][wj].index(i))
            warriors[i] = []
            continue

        warriors[i] = [wi, wj]

    return sm, attack

while True:

    # [1] 메두사 이동
    mi, mj = move_medusa()

    # print("메두사 위치 : ", (mi, mj))

    # break point: 메두사 -> 공원 최단 경로 없으면 중단 or 공원에 도착했으면 중단
    if arr[mi][mj] == 'P':
        print(0)
        break
    elif [mi, mj] == [-1, -1]:
        print(-1)
        break

    # 메두사가 이동한 칸에 전사가 있으면 전사 주금 처리
    if field[mi][mj]:
        for warr in field[mi][mj]:
            warriors[warr] = []
            field[mi][mj].pop(field[mi][mj].index(warr))

    # [2] 메두사 시선
    view = seesun_medusa()

    # [3] 전사 이동
    move_cnt, attacks = move_warriors()

    print(move_cnt, sum(rocks), attacks)

    rocks = [0 for _ in range(M+1)]

