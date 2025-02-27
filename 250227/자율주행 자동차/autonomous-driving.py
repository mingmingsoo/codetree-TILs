'''
문제설명
    1. 현재 방향 기준으로 왼쪽 방향으로 간 적 없으면 좌회전해서 1칸 간다
    2. 1번에서 이미 방문했거나 도로가 아니면 1번으로 돌아감
    3. 4방향 모두 전진하지 못하면 후진(방향 유지)
    4. 후진 못하면 끝

입력
    맵 크기
    초기 위치, 방향
    맵 (도로 0, 인도 1)
출력
    총 면적 (visited가 True 인 애들의 갯수)

구상
    조건 잘 따져야...
'''

n, m = map(int, input().split())
sr, sc, sd = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
visited = [[False] * m for i in range(n)]
visited[sr][sc] = True
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
r, c, d = sr, sc, sd
cnt = 0
while True:
    # 1. 현재 방향 기준으로 왼쪽 방향으로 간 적 없으면 좌회전해서 1칸 간다 -> 이게 근데 현재방향이 유지 되는건가?ㅠㅠ 아니라고 가정하고 풀자
    nr = r + row[(d + 3) % 4]
    nc = c + col[(d + 3) % 4]
    if not visited[nr][nc] and grid[nr][nc] == 0:
        # 이러면 갈 수 있다.
        cnt = 0
        visited[nr][nc] = True
        d = (d + 3) % 4
        r = nr
        c = nc
    else:
        # 2. 1번에서 이미 방문했거나 도로가 아니면 1번으로 돌아감
        d = (d + 3) % 4  # 방향만 바꾸기
        cnt += 1
    if cnt > 3:  # 3. 4방향 모두 전진하지 못하면 후진(방향 유지)
        nr = r - row[d]
        nc = c - col[d]
        if grid[nr][nc] == 0:
            visited[nr][nc] = True
            r = nr
            c = nc
            cnt = 0
        # 4. 후진 못하면 끝
        else:
            break

ans = 0
for _ in visited:
    ans += _.count(True)
print(ans)
