'''
문제설명
    - 나무는 가림용이다.
    - 게임
        1. 도망 (술래랑 거리 3 이하만 움직임)
            - 도망자는 좌우 혹은 상하만 있음
            - 처음은 무조건 오른쪽, 아래쪽을 보고 시작
            - in : 술래 없으면 이동
            - out : 방향전환하고 술래 없으면 이동
        2. 술래
            달팽이대로 1칸씩 이동 -> 방향과 d를 미리 담아주기
    - 점수 : 턴 * 잡은 도망자 수
구상
    - 술래 이동/방향 배열 미리 만들어놓기 - 그냥 list로
    - 도망자들은 겹쳐질 수 있으므로 3차원 배열로
    - 나무위치는 2차원 배열로 따로담기
    1. run - 도망자 이동
        - run_possible() 거리 3 이하인 애들만
    2. police - 술래 이동
        view - 술래 잡기
    0   1  2  3
    좌 상  우  하
입력
    맵 n, 도망자 수 m, 나무 수 h, 턴 수 k
    도망자 위치 x,y,d (1: 좌우, 2: 상하) -> 1씩 빼주기
    나무 위치
'''

n, runner_num, tree_num, turn_num = map(int, input().split())
tree_grid = [[0] * n for i in range(n)]
grid = [[[] for i in range(n)] for i in range(n)]
row = [0, 1, 0, -1]
col = [1, 0, -1, 0]
for rn in range(runner_num):
    r, c, d = map(lambda x: int(x) - 1, input().split())
    grid[r][c].append(d)
for tn in range(tree_num):
    r, c = map(lambda x: int(x) - 1, input().split())
    tree_grid[r][c] = 1


r, c, d = n // 2, n // 2, 0
# 방향 2차원 배열 2개 만들어놓기
s_row = [-1, 0, 1, 0]
s_col = [0, 1, 0, -1]
center_zero = [[0] * n for i in range(n)]
zero_center = [[0] * n for i in range(n)]
num, two, cnt = 1, 0, 0
while not (r == 0 and c == 0):
    center_zero[r][c] = d
    r = r + s_row[d]
    c = c + s_col[d]
    cnt += 1
    if cnt == num:
        two += 1
        d = (d + 1) % 4
        cnt = 0
    if two == 2:
        num += 1
        two = 0

center_zero[0][0] = 2

r, c, d = 0, 0, 2
visited = [[False] * n for i in range(n)]
while not (r == n // 2 and c == n // 2):
    visited[r][c] = True
    if not (0 <= r + s_row[d] < n and 0 <= c + s_col[d] < n) or visited[r + s_row[d]][c + s_col[d]]:
        d = (d + 3) % 4
    zero_center[r][c] = d
    r = r + s_row[d]
    c = c + s_col[d]

# for i in range(n):
#     for j in range(n):
#         print("↑→↓←"[center_zero[i][j]], end=" ")
#     print()
# print("-------------")
zero_center[0][0] = 2
# for i in range(n):
#     for j in range(n):
#         print("↑→↓←"[zero_center[i][j]], end=" ")
#     print()
r, c = n // 2, n // 2
score = 0


def in_three(pr, pc):
    if abs(r - pr) + abs(c - pc) <= 3:
        return True
    return False


def run():  # 도망자 이동
    global grid
    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for player_d in grid[i][j]:
                    if in_three(i, j):
                        nr = i + row[player_d]
                        nc = j + col[player_d]
                        if 0 <= nr < n and 0 <= nc < n:
                            if (nr, nc) != (r, c):
                                new_grid[nr][nc].append(player_d)
                            else:
                                new_grid[i][j].append(player_d)
                        else:
                            player_d = (player_d + 2) % 4  # 방향 틀어줌은 무조건
                            nr = i + row[player_d]  # 재계산
                            nc = j + col[player_d]
                            if (nr, nc) != (r, c):
                                new_grid[nr][nc].append(player_d)
                            else:
                                new_grid[i][j].append(player_d)
                    else:
                        new_grid[i][j].append(player_d)
    grid = new_grid


change = 0
for turn in range(1, turn_num + 1):  # 턴수마다 무슨 배열 쓸껀지 계산 필요.
    if change == 0:
        catch = 0
        # 1. run - 도망자 이동
        #     - in_three() 거리 3 이하인 애들만
        run()
        # 2. police - 술래 이동
        d = center_zero[r][c]
        nr = r + s_row[d]
        nc = c + s_col[d]
        # 2- 1. view - 술래 잡기 - 바라보는 방향은 nr,nc의 d기준임
        view_d = center_zero[nr][nc]
        # print("술래위치:", (nr, nc), "어느방향 바라보고 있는지: ", "↑→↓←"[view_d])
        for dist in range(0, 3):
            view_r = nr + s_row[view_d] * dist
            view_c = nc + s_col[view_d] * dist
            if 0 <= view_r < n and 0 <= view_c < n:
                # print(view_r, view_c)
                if not tree_grid[view_r][view_c] and grid[view_r][view_c]:
                    catch += len(grid[view_r][view_c])
                    grid[view_r][view_c] = []

        score += (turn) * catch
        r = nr
        c = nc
        if r == 0 and c == 0:
            change = 1
    else:
        catch = 0
        # 1. run - 도망자 이동
        #     - in_three() 거리 3 이하인 애들만
        run()
        # 2. police - 술래 이동
        d = zero_center[r][c]
        nr = r + s_row[d]
        nc = c + s_col[d]
        # 2- 1. view - 술래 잡기 - 바라보는 방향은 nr,nc의 d기준임
        view_d = zero_center[nr][nc]
        # print("술래위치:", (nr, nc), "어느방향 바라보고 있는지: ", "↑→↓←"[view_d])
        for dist in range(0, 3):
            view_r = nr + s_row[view_d] * dist
            view_c = nc + s_col[view_d] * dist
            if 0 <= view_r < n and 0 <= view_c < n:
                # print(view_r, view_c)
                if not tree_grid[view_r][view_c] and grid[view_r][view_c]:
                    catch += len(grid[view_r][view_c])
                    grid[view_r][view_c] = []
        score += (turn) * catch
        r = nr
        c = nc
        if r == n // 2 and c == n // 2:
            change = 0
print(score)
