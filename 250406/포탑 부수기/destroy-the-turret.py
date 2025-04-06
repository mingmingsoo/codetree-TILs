'''
문제 설명
    1. 공격자 선정
    2. 공격 대상자 선정
    3. 레이저 or 포탄 공격
    4. 정비
입력
    맵 N,M 턴수 k
    맵 정보
출력
    과정 종료 후 가장 큰 값
필요한 변수
    time_grid - 시간 기록
    battle_grid - 배틀 여부 기록
필요한 함수
    select()
    laser()
    bomb()
    restore()
4 4 1
0 1 4 4
8 0 10 13
8 0 11 26
0 0 0 0

4 4 1
1 5 0 0
0 0 0 0
0 0 0 0
0 0 0 0
'''
from collections import deque

n, m, turn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
time_grid = [[0] * m for i in range(n)]
row = [0, 1, 0, -1, 1, 1, -1, -1]
col = [1, 0, -1, 0, 1, -1, 1, -1]


def select():
    lst = []
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                lst.append((grid[i][j], -time_grid[i][j], -(i + j), -j, (i, j)))
    return lst


def restore():
    for i in range(n):
        for j in range(m):
            if not battle_grid[i][j] and grid[i][j]:
                grid[i][j] += 1


def laser(sr, sc, er, ec):
    visited = [[False] * m for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, [])])
    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            # 여기서 애들 처리
            power = grid[sr][sc]
            path.pop()  # 맨 뒤에꺼 빼
            battle_grid[er][ec] = battle_grid[sr][sc] = 1
            for ar, ac in path:
                grid[ar][ac] = max(0, grid[ar][ac] - power // 2)
                battle_grid[ar][ac] = 1
            grid[er][ec] = max(0, grid[er][ec] - power)
            return True
        for k in range(4):
            nr = (r + row[k]) % n
            nc = (c + col[k]) % m
            if visited[nr][nc] or not grid[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, path + [(nr, nc)]))
    return False


def bomb(sr, sc, er, ec):
    power = grid[sr][sc]
    battle_grid[sr][sc] = battle_grid[er][ec] = 1
    grid[er][ec] = max(0, grid[er][ec] - power)
    for k in range(8):
        nr = (er + row[k]) % n
        nc = (ec + col[k]) % m
        if (nr, nc) == (sr, sc):
            continue
        battle_grid[nr][nc] = 1
        grid[nr][nc] = max(0, grid[nr][nc] - power // 2)


for t in range(1, turn + 1):
    hoobo = select()
    if len(hoobo) <= 1:
        break
    hoobo.sort()
    battle_grid = [[0] * m for i in range(n)]
    attack = hoobo[0]
    defense = hoobo[-1]
    sp, st, sh, sj, slo = attack
    ep, et, eh, ej, elo = defense
    sr, sc = slo
    er, ec = elo
    time_grid[sr][sc] = t
    # 힘 증가
    grid[sr][sc] += (n + m)
    if not laser(sr, sc, er, ec):
        bomb(sr, sc, er, ec)
    restore()

print(max(map(max, grid)))
