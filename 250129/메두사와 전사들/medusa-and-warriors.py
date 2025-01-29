'''
세번째 풀이.. 파이썬으로 풀어보기
문제 시작 14:35
중단 16:15
재개 17:45

'''
import copy
from collections import deque

row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]
row2 = [0, 0, -1, 1]
col2 = [-1, 1, 0, 0]
n, m = map(int, input().split())  # 맵 크기 , 전사 수
sr, sc, er, ec = map(int, input().split())  # 시작점, 끝점
tmp = list(map(int, input().split()))
navyList = []
for i in range(0, m * 2, 2):
    navyList.append([tmp[i], tmp[i + 1]])

grid = [list(map(int, input().split())) for i in range(n)]

medusaStack = []


def tracePath(parentR, parentC, sr, sc, er, ec):
    r = er
    c = ec

    while r != -1 and c != -1:
        medusaStack.append((r, c))
        pR = parentR[r][c]
        pC = parentC[r][c]
        r = pR
        c = pC


def medusaBfs():
    q = deque()
    q.append((sr, sc))
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    parentR = [[-1] * n for i in range(n)]
    parentC = [[-1] * n for i in range(n)]
    while q:
        r, c = q.popleft()
        if (r == er and c == ec):
            tracePath(parentR, parentC, sr, sc, er, ec)
            return True
        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if (nr >= 0 and nr < n and nc >= 0 and nc < n and not visited[nr][nc] and grid[nr][nc] == 0):
                q.append((nr, nc))
                visited[nr][nc] = True
                parentR[nr][nc] = r  # 부모 흔적 남기기
                parentC[nr][nc] = c
    return False


def medusaWatch():
    global viewGrid
    stone = 0
    dir = "위"
    for i in range(r - 1, -1, -1):
        for j in range(i - r, r - i + 1):
            if (c + j < 0 or c + j >= n):
                continue
            viewGrid[i][c + j] = 1
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (navyR >= r):
            continue
        if(viewGrid[navyR][navyC]==0):
            continue
        elif (navyC < c):
            for i in range(navyR - 1, -1, -1):
                for j in range( i - navyR, 1):
                    if (navyC + j < 0):
                        continue
                    viewGrid[i][navyC + j] = 0
        elif (navyC == c):
            for i in range(navyR - 1, -1, -1):
                viewGrid[i][navyC] = 0
        elif (navyC > c):
            for i in range(navyR -1, -1, -1):
                for j in range(0, navyR - i + 1):
                    if (navyC + j >= n):
                        continue
                    viewGrid[i][navyC + j] = 0
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (viewGrid[navyR][navyC] == 1):
            stone += 1

    # 아래
    downGrid = [[0] * n for i in range(n)]
    for i in range(r + 1, n, 1):
        for j in range(r - i, i - r + 1):
            if (c + j < 0 or c + j >= n):
                continue
            downGrid[i][c + j] = 1

    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (navyR <= r):
            continue
        if(downGrid[navyR][navyC]==0):
            continue
        elif (navyC < c):
            for i in range(navyR + 1, n, 1):
                for j in range(navyR - i, 1):
                    if (navyC + j < 0):
                        continue
                    downGrid[i][navyC + j] = 0
        elif (navyC == c):
            for i in range(navyR + 1, n, 1):
                downGrid[i][navyC] = 0
        elif (navyC > c):
            for i in range(navyR + 1, n, 1):
                for j in range(0, i - navyR + 1):
                    if (navyC + j >= n):
                        continue
                    downGrid[i][navyC + j] = 0
    downStone = 0
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (downGrid[navyR][navyC] == 1):
            downStone += 1
    if (downStone > stone):
        stone = downStone
        viewGrid = copy.deepcopy(downGrid)
        dir = "아래"

    # 좌
    leftGrid = [[0] * n for i in range(n)]
    for j in range(c - 1, -1, -1):
        for i in range(j - c, c - j + 1):
            if (r + i < 0 or r + i >= n):
                continue
            leftGrid[r + i][j] = 1

    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (navyC >= c):
            continue
        if(leftGrid[navyR][navyC]==0):
            continue
        elif (navyR < r):
            for j in range(navyC - 1, -1, -1):
                for i in range(j - navyC, 1):
                    if (navyR + i < 0):
                        continue
                    leftGrid[navyR + i][j] = 0
        elif (navyR == r):
            for j in range(navyC - 1, -1, -1):
                leftGrid[navyR][j] = 0
        elif (navyR > r):
            for j in range(navyC - 1, -1, -1):
                for j in range(0, navyR - j + 1):
                    if (navyR + i >= n):
                        continue
                    leftGrid[navyR + i][j] = 0
    leftStone = 0
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (leftGrid[navyR][navyC] == 1):
            leftStone += 1
    if (leftStone > stone):
        stone = leftStone
        viewGrid = copy.deepcopy(leftGrid)
        dir = "왼"

    # 우
    rightGrid = [[0] * n for i in range(n)]
    for j in range(c + 1, n, 1):
        for i in range(c - j, j - c + 1):
            if (r + i < 0 or r + i >= n):
                continue
            rightGrid[i + r][j] = 1

    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (navyC <= c):
            continue
        if(rightGrid[navyR][navyC]==0):
            continue
        elif (navyR < r):
            for j in range(navyC + 1, n, 1):
                for i in range(navyC - j, 1):
                    if (navyR + i < 0):
                        continue
                    rightGrid[navyR + i][j] = 0
        elif (navyR == r):
            for j in range(navyC + 1, n, 1):
                rightGrid[navyR][j] = 0
        elif (navyR > r):
            for j in range(navyC + 1, n, 1):
                for i in range(0, j - navyC + 1):
                    if (navyR + i >= n):
                        continue
                    rightGrid[navyR + i][j] = 0
    rightStone = 0
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (rightGrid[navyR][navyC] == 1):
            rightStone += 1
    if (rightStone > stone):
        stone = rightStone
        viewGrid = copy.deepcopy(rightGrid)
        dir = "우"

    # print(dir)
    return stone


def navyGo():
    move = 0
    for navy in navyList:
        navyR = navy[0]
        navyC = navy[1]
        if (viewGrid[navyR][navyC] == 1):
            continue
        # 원래 거리 차이
        originDistance = abs(r - navyR) + abs(c - navyC)

        for k in range(4):
            nr = navyR + row[k]
            nc = navyC + col[k]
            if(nr>=0 and nr<n and nc>=0 and nc<n and viewGrid[nr][nc]==0):
                if((abs(r - nr) + abs(c - nc)) < originDistance):
                    navy[0] = nr
                    navy[1] = nc
                    move+=1
                    break

        # 두번째 이동
        navyR = navy[0]
        navyC = navy[1]
        originDistance = abs(r - navyR) + abs(c - navyC)

        for k in range(4):
            nr = navyR + row2[k]
            nc = navyC + col2[k]
            if(nr>=0 and nr<n and nc>=0 and nc<n and viewGrid[nr][nc]==0):
                if((abs(r - nr) + abs(c - nc)) < originDistance):
                    navy[0] = nr
                    navy[1] = nc
                    move +=1
                    break
    return move


def navyAttack():
    die = 0
    for i in range(len(navyList)-1,-1,-1):
        navy = navyList[i]
        navyR = navy[0]
        navyC = navy[1]
        if(navyR == r and navyC ==c):
            die+=1
            navyList.pop(i)
    return die


def medusaAttack():
    for i in range(len(navyList) - 1, -1, -1):
        navy = navyList[i]
        navyR = navy[0]
        navyC = navy[1]
        if (navyR == r and navyC == c):
            navyList.pop(i)


if (medusaBfs()):  # 메두사 최단 거리 계산 -> 불가능 하면 -1 출력
    medusaStack.pop()  # 초기값 하나 빼주기
    while medusaStack:
        r, c = medusaStack.pop()  # 메두사 이동
        if (r == er and c == ec):
            break
        medusaAttack()
        viewGrid = [[0] * n for i in range(n)]
        medusaView = medusaWatch()  # 메두사 시선
        navyMove = navyGo()  # 전사들 이동

        navyNum = navyAttack()  # 전사들 공격
        print(navyMove, medusaView, navyNum)
    print(0)

else:
    print(-1)
