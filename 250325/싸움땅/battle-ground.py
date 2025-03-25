'''
실제 시험이라고 생각하자
문제설명
    잘 이해 안돼서 타이핑 해보자
    1. 첫번째 플레이어부터 "순차적으로" 본인이 향하고 있는 방향대로 한 칸 이동
        만약 격자 밖인 경우 반대 방향으로 한 칸 이동
    2. 이동한 방향에 플레이어가 없는 경우
        - 해당 칸에 총이 있는지 확인
        - 플레이어가 총이 없고 칸에 총이 있는 경우 총 획득
        - 플레이어가 총이 있고 칸에 총이 있는 경우
            더 쎈 총을 획득하고 나머지 총은 내려놓음
        이동한 방향에 플레이어가 있는 경우
        - 초기능력치_총 공격력 합으로 싸움
             같으면 초기 능력치가 높은 프레이어가 승리
            -> 이긴 플레이어는 플레이어 초기 능력치 + 총 공격력 합의 차이만큼 포인트 획득
        -> 진 플레이어는 본인 총 내려놓고 1칸 이동
            -> 만약 다른 플레이어나 격자가 밖이면 오른쪽으로 90도 회전해서 빈칸이 보이는 순간 이동
                해당 칸에 총이 있으면 가장 공격력 높은 총 획득, 나머지는 내려놓음
        -> 이긴 플레이어는 승리한 칸에 있는 총들과 원래 총 비교해서 가장 높은 총 획득
            나머지는 내려놓음

입력
    맵 n, 플레이어ㅅ m, k 라운드 수
    맵 정보(총 정보)
    플레이어 정보

구상
    플레이어를 어떻게 관리할건지...
    플레이어 배열 : [위치,방향,초기능력치, 총공격력]
    총 배열 : 3차원 배열

필요한 메서드
    move()
        battle()

'''
n, player_num, time = map(int, input().split())
tmp = [list(map(int, input().split())) for i in range(n)]

grid = [[[] for i in range(n)] for i in range(n)]
player_grid = [[0] * n for i in range(n)]
for p in range(player_num):
    r, c, d, power = map(int, input().split())
    player_grid[r - 1][c - 1] = (p, d, power, 0)
row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
# for _ in player_grid:
#     print(_)

for i in range(n):
    for j in range(n):
        if tmp[i][j]:
            grid[i][j].append(tmp[i][j])
#
# for _ in grid:
#     print(_)

ans = [0] * player_num


def battle(win_score, win_num, win_d, win_power, win_gun, lose_num, lose_d, lose_power, lose_gun, i, j, nr, nc):
    ans[win_num] += win_score

    # 진 플레이어는 본인이 가지고 있는 총을 해당 격자에 내려놓음
    if lose_gun:
        grid[nr][nc].append(lose_gun)
        lose_gun = 0
    move = False
    for w in range(4):
        if not (0 <= nr + row[lose_d] < n and 0 <= nc + col[lose_d] < n) or \
                player_grid[nr + row[lose_d]][nc + col[lose_d]]:
            lose_d = (lose_d + 1) % 4
        else:
            move = True
            break
    if move:
        nor = nr + row[lose_d]
        noc = nc + col[lose_d]
        if grid[nor][noc]:
            lose_gun = max(grid[nor][noc])
            grid[nor][noc].remove(lose_gun)
        player_grid[nor][noc] = (lose_num, lose_d, lose_power, lose_gun)
    # 이긴 플레이어는...
    if grid[nr][nc]:
        other_gun = max(grid[nr][nc])
        if other_gun > win_gun:
            grid[nr][nc].remove(other_gun)
            grid[nr][nc].append(win_gun)  # 내 총 내려놓음
            win_gun = other_gun
    player_grid[nr][nc] = (win_num, win_d, win_power, win_gun)  # 나는 그 총 먹음


def myprint():
    print("-------------------------")
    for i in range(n):
        for j in range(n):
            if player_grid[i][j]:
                print(player_grid[i][j][0], end=" ")
            else:
                print(".", end=" ")
        print()


def move():
    for num in range(player_num):
        find = False
        for i in range(n):
            for j in range(n):
                if player_grid[i][j]:
                    pnum, d, power, gun = player_grid[i][j]
                    if pnum == num:
                        find = True
                        if not (0 <= i + row[d] < n and 0 <= j + col[d] < n):
                            d = (d + 2) % 4
                        nr = i + row[d]
                        nc = j + col[d]
                        if not player_grid[nr][nc]:  # 다른 플에이어가 없으면
                            # 해당 칸에 총이 있는지 확인
                            if grid[nr][nc]:
                                other_gun = max(grid[nr][nc])
                                if other_gun > gun:
                                    grid[nr][nc].remove(other_gun)
                                    if gun != 0:
                                        grid[nr][nc].append(gun)  # 내 총 내려놓음
                                    gun = other_gun
                            player_grid[nr][nc] = (pnum, d, power, gun)  # 나는 그 총 먹음
                            player_grid[i][j] = 0  # 나는 떠났음

                        else:  # 다른 플레이어 있으면 싸운다.
                            my_power = power + gun
                            o_pnum, o_d, o_power, o_gun = player_grid[nr][nc]
                            other_power = o_power + o_gun
                            if my_power > other_power:  # 내가 이김!
                                win_num, win_d, win_power, win_gun = pnum, d, power, gun
                                lose_num, lose_d, lose_power, lose_gun = o_pnum, o_d, o_power, o_gun
                            elif my_power == other_power:
                                if power > o_power:
                                    win_num, win_d, win_power, win_gun = pnum, d, power, gun
                                    lose_num, lose_d, lose_power, lose_gun = o_pnum, o_d, o_power, o_gun
                                else:
                                    win_num, win_d, win_power, win_gun = o_pnum, o_d, o_power, o_gun
                                    lose_num, lose_d, lose_power, lose_gun = pnum, d, power, gun
                            elif my_power < other_power:
                                win_num, win_d, win_power, win_gun = o_pnum, o_d, o_power, o_gun
                                lose_num, lose_d, lose_power, lose_gun = pnum, d, power, gun
                            win_score = abs(my_power - other_power)
                            player_grid[i][j] = 0  # 나는 떠났음
                            battle(win_score, win_num, win_d, win_power, win_gun, lose_num, lose_d, lose_power,
                                   lose_gun, i, j, nr, nc)
                        break
            if find:
                break

for t in range(time):
    move()
    # myprint()
print(*ans)
