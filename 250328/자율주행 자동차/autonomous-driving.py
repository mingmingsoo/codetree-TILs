'''
문제 설명
    1. 현재 d 기준 왼쪽 회전으로 간 적 없으면 인도일 경우 간다
        - 만약 인도거나 이미 간 곳이면 다시 좌회전
        - 4바퀴 다 돌았는데 못가면 방향 유지한 채 후진
    2. 다시 1번
        - 후진까지 못하면 끝.

입력
    맵 크기 n,m
    초기 r,c,d (0123 북동남서)
    맵 정보
        인도는 1
        테투리는 모두 1
'''

n, m = map(int, input().split())
r, c, d = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

visited = [[False] * m for i in range(n)]
visited[r][c] = True
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
while True:
    # 1. 현재 d 기준 왼쪽 회전으로 간 적 없으면 인도일 경우 간다
    #     - 만약 인도거나 이미 간 곳이면 다시 좌회전
    move = False
    for k in range(4):
        d = (d + 3) % 4
        nr = r + row[d]
        nc = c + col[d]
        if not visited[nr][nc] and grid[nr][nc] == 0:
            move = True
            visited[nr][nc] = True
            r = nr
            c = nc
            break
    #     - 4바퀴 다 돌았는데 못가면 방향 유지한 채 후진
    if not move:
        back = False
        if not move:
            nr = r - row[d]
            nc = c - col[d]
            if grid[nr][nc] == 0:
                visited[nr][nc] = True
                back = True
                r = nr
                c = nc
        if not back:
            break

print(sum(map(sum, visited)))