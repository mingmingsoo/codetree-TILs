'''
시간복잡도
턴수 1000 * 말 수 10
ㄱㅊ
'''
n, horse_num = map(int, input().split())
grid = [[2] * (n + 2)] + [[2] + list(map(int, input().split())) + [2] for i in range(n)] + [[2] * (n + 2)]
n += 2
horse_grid = [[[] for i in range(n)] for i in range(n)]
horse_list = [0]
for h in range(1, horse_num + 1):
    r, c, d = map(int, input().split())
    horse_grid[r][c].append(h)
    horse_list.append([r, c, d - 1])
ans = -1
row = [0, 0, -1, 1]
col = [1, -1, 0, 0]
change_dir = [1, 0, 3, 2]
end = False
for time in range(1, 1001):
    for idx, horse in enumerate(horse_list):
        if idx == 0:
            continue
        r, c, d = horse
        nr = r + row[d]
        nc = c + col[d]
        if grid[nr][nc] == 2:
            d = change_dir[d]
            horse_list[idx][2] = d
        # 재계산
        r, c, d = horse
        nr = r + row[d]
        nc = c + col[d]
        if grid[nr][nc] == 2:
            continue  # 그래도 파란색이면 넘어가.

        # 나랑 같이 이동해야되는 내 위에 애들...
        move_lst = []
        for w in range(len(horse_grid[r][c])):
            if horse_grid[r][c][w] == idx:
                move_lst = horse_grid[r][c][w:]
                horse_grid[r][c] = horse_grid[r][c][:w]
                break
        if grid[nr][nc] == 1:
            move_lst.reverse()  # 반대!
        horse_grid[nr][nc].extend(move_lst)
        if len(horse_grid[nr][nc]) >= 4:
            end = True
            ans = time
            break
        for midx in move_lst:
            horse_list[midx][0] = nr
            horse_list[midx][1] = nc

    if end:
        break
print(ans)
