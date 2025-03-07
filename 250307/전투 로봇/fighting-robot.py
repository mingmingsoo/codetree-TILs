'''
문제설명
    초기 전투로봇 레벨2
    1초에 상하좌우 한칸식 이동
    자기보다 레벨 높은애들은 지나갈 수 없음
    자기보다 레벨 낮은애들 없앨 수 있음
    자기랑 레벨 같으면 지나갈 수 는 있음
    가는 우선순위
    1. 거리가 가장 가까운
    2. 가장 위쪽, 왼쪽
    없으면 끝
    전투로봇은 본인 레벨만큼 먹으면 레벨 상승함

입력
    9: 전투로봇
    1~6 : 몬스터
구상
    bfs도는데 힙큐 사용.

'''
import heapq
from collections import deque

n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

r, c, level, eat = -1, -1, 2, 0
for i in range(n):
    for j in range(n):
        if grid[i][j] == 9:
            grid[i][j] = 0
            r, c = i, j

time = 0
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]
while True:
    # 자기보다 레벨 높은애들은 지나갈 수 없음
    # 자기보다 레벨 낮은애들 없앨 수 있음
    # 자기랑 레벨 같으면 지나갈 수 는 있음
    target_q = []

    # 아 거리 계산하는게 쉽지 않네...

    q = deque([(r, c, 0)])
    visited = [[False] * n for i in range(n)]
    visited[r][c] = True
    while q:
        r, c, dist = q.popleft()

        for k in range(4):
            nr = r + row[k]
            nc = c + col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc]:
                continue
            if grid[nr][nc] == 0 or grid[nr][nc] == level:
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
            elif grid[nr][nc] < level:
                visited[nr][nc] = True
                heapq.heappush(target_q, (dist + 1, nr, nc))
    if not target_q:
        break
    # print(target_q)
    dist, target_r, target_c = heapq.heappop(target_q)
    # print((target_r,target_c),dist)
    grid[target_r][target_c] = 0  # 먹는다
    eat += 1
    r = target_r
    c = target_c
    time += dist
    if eat == level:
        level += 1
        eat = 0

print(time)
