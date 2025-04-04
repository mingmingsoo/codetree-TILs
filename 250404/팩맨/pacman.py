'''
최악컨디션에서 함 해부자~
문제 설명
    1. 몬스터 복제
    2. 몬스터 이동 new_grid 필요
        시체 검사 필요
    3. 팩맨 이동
        maxi = 0, nr = r ,nc = c , eating = set()
        for d1,d2,d3 in dir_lst:
            visited = set()
            if nr = ..
            if len(visited) > maxi:
                ...
        r = nr , c = nc , eating
    4. 시체 남기기 die_grid 필요
    4. die_grid 1씩 빼주기 양수인 애들만
    5. 위에 원본 extend

입력
    몬스터 마리 수 m, 진행 턴 수 t
    팩맨 위치 r,c
    몬스터 정보
주의
    팩맨 방향 우선순위 상좌하우
    set 순서 유지 되지?
    근데 팩맨이 먹을 수 있는게 하나도 없으면 이동해????????????????????????
    ㅇㅇ 그럴 듯
1 1
3 1
1 1 5
'''
p_row = [-1, 0, 1, 0]
p_col = [0, -1, 0, 1]

dir_lst = set()
sel = [0] * 3


def make_dir(idx):
    if idx == 3:
        dir_lst.add(tuple(sel))
        return
    for i in range(4):
        sel[idx] = i
        make_dir(idx + 1)


make_dir(0)
n = 4
m, time = map(int, input().split())
pr, pc = map(lambda x: int(x) - 1, input().split())
grid = [[[] for i in range(n)] for i in range(n)]
die_grid = [[0] * n for i in range(n)]
for _ in range(m):
    r, c, d = map(lambda x: int(x) - 1, input().split())
    grid[r][c].append(d)

m_row = [-1, -1, 0, 1, 1, 1, 0, -1]
m_col = [0, -1, -1, -1, 0, 1, 1, 1]

for t in range(time):
    #     2. 몬스터 이동 new_grid 필요
    #         시체 검사 필요
    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for d in grid[i][j]:
                    move = False
                    for k in range(8):
                        nr = i + m_row[d]
                        nc = j + m_col[d]
                        if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) == (pr, pc) or die_grid[nr][nc]:
                            d = (d + 1) % 8
                        else:
                            move = True
                            break
                    if move:
                        nr = i + m_row[d]
                        nc = j + m_col[d]
                        new_grid[nr][nc].append(d)
                    else:
                        new_grid[i][j].append(d)
    location_lst = []
    for dirs in dir_lst:
        r, c = pr, pc
        eat = 0
        possible = True
        visited = set()
        for d in dirs:
            nr = r + p_row[d]
            nc = c + p_col[d]
            if not (0 <= nr < n and 0 <= nc < n):
                possible = False
                break
            if new_grid[nr][nc] and (nr, nc) not in visited:
                visited.add((nr, nc))
                eat += len(new_grid[nr][nc])
            r = nr
            c = nc
        if possible:
            location_lst.append((-eat, dirs, visited, r, c))
    location_lst.sort()
    eat_num, dirs, eating, npr, npc = location_lst[0]
    pr, pc = npr, npc  # 팩맨 이동
    for r, c in eating:
        new_grid[r][c] = []  # 먹혔다.
        die_grid[r][c] = 3  # 죽었다

    #     4. die_grid 1씩 빼주기 양수인 애들만
    for i in range(n):
        for j in range(n):
            if die_grid[i][j]:
                die_grid[i][j] -= 1

    #     5. 위에 원본 extend
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                new_grid[i][j].extend(grid[i][j])
    grid = new_grid

ans = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            ans += len(grid[i][j])
print(ans)
