'''
코드트리 정육면체 굴리기 1626~
문제설명
    1. 정육면체를 굴리는데 격자판이 0이면 주사위 바닥면에 쓰여있는 수가 격자판에 복사
    2. 격자판이 0이아니면 칸에 쓰여있는 수가 주사위 바닥에 복사되고 그 칸은 0이됨
    3. 격자판 밖으로 이동하라는 명령은 무시

입력
    n,m 정육면체 처음위치 x,y, 굴리는 횟수 k
    격자판 정보
    1  2  3  4
    동 서 북 남
출력
    매 이동마다 주사위 상단에 쓰여있는 숫자 출력
구상
    성실히 구현....
'''

n, m, r, c, d_num = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
d_list = list(map(lambda x: int(x) - 1, input().split()))
row = [0, 0, -1, 1]
col = [1, -1, 0, 0]
dice = [0, 0, 0, 0, 0, 0]


#  0: 위 1: 밑 2: 앞 3: 뒤 4:왼 5:오
def roll(d):
    global dice
    if d == 0:
        dice = [dice[4], dice[5], dice[2], dice[3], dice[1], dice[0]]
    elif d == 1:
        dice = [dice[5], dice[4], dice[2], dice[3], dice[0], dice[1]]
    elif d == 2:
        dice = [dice[2], dice[3], dice[1], dice[0], dice[4], dice[5]]
    elif d == 3:
        dice = [dice[3], dice[2], dice[0], dice[1], dice[4], dice[5]]


for d in d_list:
    # 3. 격자판 밖으로 이동하라는 명령은 무시
    if not (0 <= r + row[d] < n and 0 <= c + col[d] < m):
        continue
    nr = r + row[d]
    nc = c + col[d]

    # 1. 정육면체를 굴리는데 격자판이 0이면 주사위 바닥면에 쓰여있는 수가 격자판에 복사
    roll(d)
    if grid[nr][nc] == 0:
        grid[nr][nc] = dice[1]
    # 2. 격자판이 0이아니면 칸에 쓰여있는 수가 주사위 바닥에 복사되고 그 칸은 0이됨
    else:
        dice[1] = grid[nr][nc]
        grid[nr][nc] = 0
    r = nr
    c = nc
    print(dice[0])
