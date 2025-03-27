'''
사랑들을 1차원 리스트로 관리하려다가
    최소 사각형 구할 때,,, 이 좌표를 가지는 사람이 있냐? 조회 연산이 필요해서 안썼다.
    그리고 회전도 따로 해줘야해서 안했음. 3차원 배열로 하면 맵 회전시킬때 같이 시키면 되기 때문
    
문제 설명
    N*N
    1. 참가자 이동(동시) - new_grid 필요 3차원 배열
        (sr,sc) - (er,ec) 맨하튼 최단거리 - bfs 가 아니다
         for k in range(4) 돌면서 현재 거리보다 가까우면 바로 break 하고 이동
        move = True면 ans 에 더해준다. -> len(grid[i][j]) 더해주면 됨.

        - 참가자는 grid 에 10부터 인덱싱을 남겨준다.

    2. 미로 회전
        한명 이상 참가자 & 출구를 포함하는 가장 작은 정사각형임
        크기는 2~N까지가 될 거다.
        벽이 있었으면 내구도가 1씩 깎인다
        여기서 5중 포문이 필요하긴 한데,,, 발견시 튀는거라 ㄱㅊ을 듯
    - 주의
        모든 참가자 탈출시 게임 끝 : 확인해주는 로직 필요
입력
    맵크기 n 사람 수 m 시간 k
    사람 좌표
    출구 좌표
    좌표 -1 씩 필요
출력
    이동 거리 합, 출구좌표는 -1로 하겠음
    
- 필요한 변수
    grid, new_grid = 3차원 배열
    move_possible = boolean 변수 (이동할 수 있냐? True 면 답에 더해줌)
    people_have, exit_have = boolean 변수 (회전시 이 두개 만족해야 그 사각형으로 선택해 줄 것임)
    people_exit = [False]* 사람 수 = 다 탈출 했는지
- 필요한 함수
    move() : 참가자 이동
    rotation() : 미로 회전
    all_exit() : 다 탈출했는지 확인

-ㅇㅋㅇㅋ 출구는 빈공간, 참가자 좌표랑 겹치지 않음

사람이 0,0 출구가 n-1,n-1 일떄 인덱스 에러 안나는지 확인 필요
사람이 한명이라도 있으면 사각형 생기는지 확인 필요


참가자 0,0 이고 출구가 n-1,n-1인 경우 인덱스 에러 안나는지
5 1 1
0 1 0 0 0
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
1 1
5 5


두 명의 사람이 같은 곳에 잘 있는지
5 2 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
4 5
5 5
1 5

break 잘 되는지
5 3 100
0 0 0 0 1
9 2 2 0 0
0 1 0 1 0
0 0 0 1 0
0 0 0 0 0
1 3
3 1
3 5
3 3
'''
# ------------------- 입력 ----------------------------
n, people_num, time = map(int, input().split())
block = [list(map(int, input().split())) for i in range(n)]

grid = [[[] for i in range(n)] for i in range(n)]

p_idx = 10
for p in range(people_num):
    r, c = map(int, input().split())
    grid[r - 1][c - 1].append(p_idx)
    p_idx += 1

er, ec = map(lambda x: int(x) - 1, input().split())
block[er][ec] = -1

people_exit = [False] * (people_num)
ans = 0

row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]


# ------------------- 함수 ----------------------------
def move():
    global ans, grid
    new_grid = [[[] for i in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                move = False
                cur = abs(er - i) + abs(ec - j)
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if not (0 <= nr < n and 0 <= nc < n) or block[nr][nc] > 0:  # 벽만 못간다
                        continue
                    next = abs(er - nr) + abs(ec - nc)
                    if next < cur:
                        move = True
                        if (nr, nc) == (er, ec):  # 만약 출구면
                            for pidx in grid[i][j]:
                                people_exit[pidx - 10] = True
                            ans += len(grid[i][j])  # 값만 더해주고 안넣어준다
                        else:
                            new_grid[nr][nc].extend(grid[i][j])
                            ans += len(grid[i][j])
                        break
                if not move:  # 움직이지 못했으면 그냥 원래 그자리
                    new_grid[i][j].extend(grid[i][j])
    grid = new_grid


def rotation():
    global er, ec
    L, R, C = 0, 0, 0
    for length in range(2, n + 1):  # 사각형 크기
        is_length = False
        for r in range(0, n - length + 1):
            for c in range(0, n - length + 1):
                people_have, exit_have = False, False
                # 내가 선택한 사각형
                for i in range(r, r + length):
                    for j in range(c, c + length):
                        if block[i][j] == -1:
                            exit_have = True
                        if grid[i][j]:
                            people_have = True
                if people_have and exit_have:
                    is_length = True
                    L, R, C = length, r, c
                    break
            if is_length:
                break
        if is_length:
            break

    small_block = [_[C:C + L] for _ in block[R:R + L]]
    small_grid = [[__[:] for __ in _[C:C + L]] for _ in grid[R:R + L]]

    small_lo_block = [[0] * L for i in range(L)]
    small_lo_grid = [[[] for i in range(L)] for i in range(L)]

    for i in range(L):
        for j in range(L):
            small_lo_block[i][j] = small_block[L - j - 1][i]
            small_lo_grid[i][j] = small_grid[L - j - 1][i][:]

    for i in range(L):
        for j in range(L):
            if small_lo_block[i][j] > 0:
                small_lo_block[i][j] -= 1
            block[i + R][j + C] = small_lo_block[i][j]
            grid[i + R][j + C] = small_lo_grid[i][j][:]
            if block[i + R][j + C] == -1:
                er, ec = i + R, j + C


def all_exit():
    for pepple in people_exit:
        if not pepple:
            return False
    return True


# ------------------- 메인 ----------------------------
for t in range(time):

    move()
    rotation()  # er,ec 갱신 필요
    if all_exit():
        break
print(ans)
print(er + 1, ec + 1)
