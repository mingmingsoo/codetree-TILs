'''
# 체감난이도 플5

# 문제 풀고 나서 기록
    제출 횟수 1회
    문제 시작 14:00
    문제 종료 15:13

    총 풀이시간 63분
        00~08   : 문제 이해 및 손코딩(8)
                    메두사, 전사 방향별 딕셔너리 손으로 만들고 들어가기
        08~13   : 손코딩 기반 초기 주석 및 필요한 변수/함수 세분화(5)
        13~17   : 메두사, 전사 방향별 딕셔너리 생성(4)
        17~19   : 입력받기(2)
        20~24   : 메두사 경로 bfs(4)
                    일단 경로가 무조건 return 된다고 생각하고 코드 작성
                    왜냐하면 단락이 생기는데... 단락 많은게 싫거든요
                    "코드 다 짜고 바꾸기" 라고 주석 달아놨음

                    경로에 처음 위치도 받아줬었는데 메두사 이동 후 발생하는 일들이여서
                    처음 위치는 path에서 안받아줌

        24~26   : 메두사 이동 후 전사 있으면 없애는 로직 작성(2)
        26~31   : 메두사 시야 bfs 로직 작성(5)
                    생각해보니까 메두사 시야는 visited를 쓸 필요가 없고
                    view_grid로 쓰면 된다. -> 수정!
        31~34   : 메두사 시야 bfs 로직 확인(3)
                    오잉 메두사 (1,2)에 있는데 찍히는 거 보니까 (1,3) 의 시야임
                    메두사 bfs에서 sr,sc -> r,c 로 수정!
        34~38   : 메두사와 전사의 상대적인 위치, 메두사 시야 방향을 고려해 부호를 반환해주는 로직 작성(4)
        38~40   : 전사 시야 bfs 로직 작성(2)
        40~44   : 전체적인 시야 잘 되는지 확인(4)
                    (1)
                    전사가 안가려주네?
                    -> 전사는 메두사랑 반대로 view_grid가 false면 continue 되야함! 수정!
                    (2)
                    테케 맵은 작아서 큰 맵 만들어서 시야 되는지 확인
        44~48   : 돌 많은 방향 선택하는 로직 작성(4)
                    리스트에 담아서 sort하기
        48~53   : 전사 이동 로직 작성(5)
        53~56   : 전사 이동 로직 확인(3)
                    2칸이동 할 수 있는애가 1칸 밖에 못감
                    메두사 위치는 view_grid가 False여야 전사들이 갈 수 있음!
                    메두사 위치는 시야영역에서 제외시켜줌
        56~58   : 전사 공격 로직 작성, 오픈 테케 답 나오는 거 확인(2)
        58~09   : 검증 시작(11)
                    문제 예시 테케 만들어보고 동일한 시야, 동일한 돌을 가지는지 확인
        09~13   : 문제 설계시 적어놨던 "코드 다 짜고 바꾸기"(4)
                    path 가 -1 이 아닐때만 로직 실행되게끔 수정
                    -> 진짜 -1만 출력되는지 확인

  메모리 25 MB
  시간 381 ms

    회고
        1. 자바로 풀었을 때는 시야를 bfs로 안하고 2중 포문으로 계산했었는데
            온풍기 안녕을 풀고 나서 '메두사가 온풍기 안녕 유사문제였구나' 생각이 들었었다...
            그래서 이번에는 온풍기 안녕처럼 방향별 딕셔너리를 만들어줬다.
            잔상이 있어서 빨리 풀었지만.... 처음 풀이 8시간 걸렸던 문제...
            아마 처음 풀었으면 문제 이해도 어려웠을 것이다.ㅠㅠㅠㅠㅠㅠㅠㅠㅠ
            다른 친구들보다 기출문제 푼 횟수가 적은거니 앞으로 백준, swea 모의 기출 열심히 풀자.........ㅠㅠㅜㅜㅜㅠㅠㅠㅠㅠㅠ



# 문제 풀면서의 기록
코드리팩토링, 함수화

문제 설명
    1. 메두사 이동 -> 경로 없으면 -1 출력하고 끝
        한칸씩 공원을 향해서
        간 곳에 전사 있으면 kill
        bfs
    2. 메두사 시선 -> 많이 돌 시킬 수 있고, 상하좌우 우선순위(돌 된 수)
        bfs
        dict 생성
    3. 전사 이동
        총 두 칸 이동
        (1) 거리가 줄고 상하좌우
        (2) 거리가 줄고 좌우상하
        단 메두사 시야들어오는 곳으론 못감
    4. 전사 공격(이동거리 계산 필요)
        메두사 있는 위치랑 겹치면 전사가 쥬금(전사 수 계산 필요)
입력
    맵 크기 n, 전사 수 m
    메두사 집, 공원 좌표
    전사 정보
    맵 정보
출력
    전사 이동 거리 합/ 돌 된 수/ 메두사를 공격한 전사 수
필요한 함수
    path_bfs() : 메두사 이동 경로
    medusa_bfs() : 메두사 시야
    junsa_bfs() : 전사 시야
필요한 변수
    view_grid = 불리언 2차배열
    medusa_dict = 메두사 시야 방향 딕셔너리
    junsa_dict = 전사 시야 방향 딕셔너리
시야확인용
9 3
0 3 0 5
4 2 4 4 6 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0


9 6
4 3 4 5
2 2 4 2 4 5 4 6 4 7 4 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0

9 3
4 3 4 5
6 3 7 2 8 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0



메두사 공원 못가
5 1
0 0 4 4
3 3
0 0 1 0 0
0 0 1 0 0
1 1 1 0 0
0 0 0 0 0
0 0 0 0 0



'''
# --------------------------------- 입력 ---------------------------------
from collections import deque

srow = [-1, -1, 0, 1, 1, 1, 0, -1]
scol = [0, 1, 1, 1, 0, -1, -1, -1]

# 방향별 메두사 시야
medusa_dict = {0: (7, 0, 1), 1: (3, 4, 5), 2: (5, 6, 7), 3: (1, 2, 3)}
# 메두사 방향, 전사 위치별 시야
junsa_dict = {(0, -1): (7, 0), (0, 0): (0,), (0, 1): (0, 1),
              (1, -1): (5, 4), (1, 0): (4,), (1, 1): (4, 3),
              (2, -1): (7, 6), (2, 0): (6,), (2, 1): (6, 5),
              (3, -1): (1, 2), (3, 0): (2,), (3, 1): (2, 3)}

n, junsa_num = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
junsa_lst = []
tmp = list(map(int, input().split()))

for junsa in range(0, junsa_num * 2, 2):
    junsa_lst.append([tmp[junsa], tmp[junsa + 1]])
grid = [list(map(int, input().split())) for i in range(n)]

# 전사 이동 방향  상하좌우       좌우상하
move_row = [[-1, 1, 0, 0], [0, 0, -1, 1]]
move_col = [[0, 0, -1, 1], [-1, 1, 0, 0]]


# --------------------------------- 함수 ---------------------------------
def bfs(sr, sc, er, ec):  # 메두사 경로 bfs
    bfs_row = [-1, 1, 0, 0]
    bfs_col = [0, 0, -1, 1]
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, [])])
    while q:
        r, c, path = q.popleft()
        if (r, c) == (er, ec):
            return path
        for k in range(4):
            nr = r + bfs_row[k]
            nc = c + bfs_col[k]
            if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, path + [(nr, nc)]))

    return -1


def medusa_bfs(v, r, c):  # 메두사 시야 bfs
    # v 가 방향
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        for k in medusa_dict[v]:
            nr = r + srow[k]
            nc = c + scol[k]
            if not (0 <= nr < n and 0 <= nc < n) or view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = True  # 볼 수 있어
            q.append((nr, nc))


def junsa_view(jr, jc, v, d):  # 전사 시야 bfs
    q = deque([(jr, jc)])
    while q:
        r, c = q.popleft()
        for k in junsa_dict[(v, d)]:
            nr = r + srow[k]
            nc = c + scol[k]
            if not (0 <= nr < n and 0 <= nc < n) or not view_grid[nr][nc]:
                continue
            view_grid[nr][nc] = False  # 아니 볼 수 없어
            q.append((nr, nc))


def booho(nx, x):  # 부호를 반환
    if nx < x:
        return -1
    elif nx == x:
        return 0
    elif nx > x:
        return 1


path = bfs(sr, sc, er, ec)
if path == -1:  # 공원 못가
    print(-1)
else:

    for r, c in path:
        # 메두사 위치가 지금 r,c
        if (r, c) == (er, ec):
            print(0)
            break
        move_dist, stone, attack = 0, 0, 0

        # 죽는 애 검사
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                junsa_lst.pop(i)  # 메두사가 죽임

        # 메두사 시야
        view_lst = []  # 돌이 된 전사 수 , 방향, 2차원 배열 맵
        for v in range(4):
            view_grid = [[False] * n for i in range(n)]
            medusa_bfs(v, r, c)
            for jr, jc in junsa_lst:
                if view_grid[jr][jc]:
                    if v in (0, 1):
                        junsa_view(jr, jc, v, booho(jc, c))
                    elif v in (2, 3):
                        junsa_view(jr, jc, v, booho(jr, r))

            # 여기서 갯수세서 넣어주자
            doll_cnt = 0
            for jr, jc in junsa_lst:
                if view_grid[jr][jc]:
                    doll_cnt += 1

            view_lst.append((-doll_cnt, v, view_grid))  # 깊은복사 안해줘도 된다.

        view_lst.sort()
        doll, d, view = view_lst.pop(0)
        stone += abs(doll)

        # 전사들 이동
        for idx, junsa in enumerate(junsa_lst):
            if view[junsa[0]][junsa[1]]:  # 돌이여유
                continue
            # 총 두번의 이동
            for turn in range(2):
                jr, jc = junsa_lst[idx]
                cur = abs(jr - r) + abs(jc - c)
                for k in range(4):
                    nr = jr + move_row[turn][k]
                    nc = jc + move_col[turn][k]
                    next = abs(nr - r) + abs(nc - c)
                    if (0 <= nr < n and 0 <= nc < n) and next < cur and not view[nr][nc]:
                        # 움직일 수 있다!
                        move_dist += 1
                        junsa_lst[idx][0] = nr
                        junsa_lst[idx][1] = nc
                        break

        # 전사 공격
        for i in range(len(junsa_lst) - 1, -1, -1):
            jr, jc = junsa_lst[i]
            if (r, c) == (jr, jc):
                attack += 1
                junsa_lst.pop(i)  # 전사 주금

        print(move_dist, stone, attack)
