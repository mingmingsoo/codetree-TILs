'''
attack 함수가 불필요해서 제거하고 restore 함수를 만들어줌
코드 가독성을 높혀보자!

문제 설명
    1. 공격자 선정
        우선순위
        1. 공격력 약한
        2. 최근에 공격한
        3. 행/열 합 큰
        4. 열 큰
    2. 공격당하는애 선정
        공격자와 반대
    -> 후보들을 다 넣어서 sort하고
        공격자는 0번째, 공격당하는애는 -1번째임
    -> 최근에 공격한을 알기 위해서 time_grid 생성 공격한애는 얘를 time으로 바꿔줌 즉 큰 값 우선순위가 될 것임

    3. 공격 - 모두 도넛
    - 레이저 공격 : 최단경로 - bfs
    - 포탄 공격 : 레이저 안되면 즉 path 없으면 포탄 공격 실행

    4. 포탑 정비
        공격과 무관했던 애들 +=1
        얘를 위해서 battle_grid 필요

필요한 변수
    time_grid : 최근 공격 기록
    battle_grid : 배틀 여부 기록
    player_lst : 공격자 선정
    t : 지금 몇번째 턴인지 int 변수
필요한 함수
    who_battle : 공격자/ 공격당하는애 선정
    attack : 공격
        - laser : 레이저
        - bomb : 포탑
    restore : 포탑 정비
    check : 하나만 남았냐?
주의할점
    포탑 하나만 남으면 턴 수 남아도 끝임
    n,m 다른 테케 넣어보기
    범위 조심

break 되는지
4 4 1000
0 1 4 4
8 0 10 13
8 0 11 26
0 0 0 0

n,m 다른
3 4 1
0 1 4 4
8 0 10 13
8 0 11 26

공격자는 포탄 공격 안받는지
3 3 1
1 0 0
0 5 0
0 0 0

'''
from collections import deque


def who_battle(): # 공격자, 공격대상자 정하는 함수
    player_lst = []
    for i in range(n):
        for j in range(m):
            if grid[i][j]:
                player_lst.append((grid[i][j], -time_grid[i][j], -(i + j), -j, (i, j)))
    player_lst.sort()
    return player_lst


def laser_attack(start, end, power): # 레이저 공격 함수
    sr, sc, er, ec = start[0], start[1], end[0], end[1]
    q = deque([(sr, sc, [(sr, sc)])])  # 경로 담고 er,ec 도달하면 걔네들 위치 다 battle_grid true해줌
    visited = [[False] * m for i in range(n)]
    visited[sr][sc] = True

    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            for x, y in path:
                battle_grid[x][y] = True
                if (x, y) == (er, ec): # 공격 대상자는 그대로
                    grid[x][y] -= power
                    if grid[x][y] < 0: grid[x][y] = 0
                if (x, y) != (er, ec) and (x, y) != (sr, sc): # 공격대상자도 아니고 공격자도 아닌 애들은 절반만
                    grid[x][y] -= power // 2
                    if grid[x][y] < 0:  grid[x][y] = 0
            return True
        for k in range(4):
            nr = (r + row[k]) % n
            nc = (c + col[k]) % m
            if visited[nr][nc] or grid[nr][nc] == 0: continue
            visited[nr][nc] = True
            q.append((nr, nc, path[:] + [(nr, nc)]))

    return False


def bomb_attack(start, end, power):
    sr, sc, er, ec = start[0], start[1], end[0], end[1]

    grid[er][ec] -= power
    if grid[er][ec] < 0: grid[er][ec] = 0
    battle_grid[sr][sc] = battle_grid[er][ec] = True
    for k in range(8):
        nr = (er + row[k]) % n
        nc = (ec + col[k]) % m
        if grid[nr][nc] == 0: continue
        battle_grid[nr][nc] = True
        if (nr, nc) != (sr, sc):
            grid[nr][nc] -= power // 2
            if grid[nr][nc] < 0: grid[nr][nc] = 0


def restore():
    for i in range(n):
        for j in range(m):
            if not battle_grid[i][j] and grid[i][j] > 0:
                grid[i][j] += 1


n, m, time = map(int, input().split())

grid = [list(map(int, input().split())) for i in range(n)]
time_grid = [[0] * m for i in range(n)]

# 우 하 좌 상         # 포탄용
row = [0, 1, 0, -1, 1, 1, -1, -1]
col = [1, 0, -1, 0, 1, -1, 1, -1]

for t in range(1, time + 1):
    battle_grid = [[False] * m for i in range(n)]
    player_lst = who_battle()  # 이거 한명만 남았을 때 확인해야함 none return 안하는지 확인
    if len(player_lst) < 2:  # 1명밖에 없거나 0명이면 게임 끝!! 배틀할 수가없음.
        break
    start = player_lst[0][4]
    end = player_lst[-1][4]
    time_grid[start[0]][start[1]] = t  # 최근에 공격했다.
    grid[start[0]][start[1]] += n + m
    power = player_lst[0][0] + n + m
    if not laser_attack(start, end, power):
        bomb_attack(start, end, power)
    restore()

print(max(map(max, grid)))
