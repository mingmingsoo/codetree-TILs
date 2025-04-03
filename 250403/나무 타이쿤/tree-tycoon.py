'''
왤케 어후 설명이 어려워
문제 설명
    - 초기: 영양제 왼,아래에 4개 -> set
    for 년수
        1. 영양제 이동 (도넛)
        2. 영양제 해당되는 애들 대각선 4방에 1 이상인 갯수만큼 성장(도넛X) -> new_grid 필요
        3. 기존 set 제외하고 맵에서 2 이상인 애들 -2 하고 영양제 new_set 에 담아줌
            set = new_set
입력
    맵 크기 n 총 년수 time
    맵 정보
    이동 규칙 d, l (방향 길이)
출력
    그리드 합
'''

n, time = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
nutrition = [[n - 1, 0], [n - 1, 1], [n - 2, 0], [n - 2, 1]]

row = [0, -1, -1, -1, 0, 1, 1, 1]
col = [1, 1, 0, -1, -1, -1, 0, 1]

for t in range(time):
    d, l = map(int, input().split())
    d -= 1
    for idx, location in enumerate(nutrition):
        r, c = location
        nr = (r + row[d] * l) % n
        nc = (c + col[d] * l) % n
        grid[nr][nc] += 1
        nutrition[idx][0] = nr
        nutrition[idx][1] = nc
    plus_grid = [[0] * n for i in range(n)]

    for r, c in nutrition:
        cnt = 0
        for k in (1, 3, 5, 7):
            nr = r + row[k]
            nc = c + col[k]
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
                cnt += 1
        plus_grid[r][c] += cnt

    for i in range(n):
        for j in range(n):
            if plus_grid[i][j]:
                grid[i][j] += plus_grid[i][j]

    new_nutrition = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= 2 and [i, j] not in nutrition:
                grid[i][j] -= 2
                new_nutrition.append([i, j])

    nutrition = new_nutrition

print(sum(map(sum, grid)))