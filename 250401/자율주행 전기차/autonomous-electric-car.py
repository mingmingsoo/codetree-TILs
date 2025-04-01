'''
처음보는 문제라 생각하자
문제 설명이 좀 정신 없는데
    1. 내 위치에서 최단 거리 승객 태운다 (위.왼)
    2. 목적지 까지 데려다준다
        - > 이동한 거리만큼 베터리 충전
        -> 가는 길에 엔꼬나면 -1 출력
    3. 베터리 충전은 태우고 나서의 거리만큼 * 2 충전된다 풀 거리가 아니다.
입력
    맵 크기 N, 승객 수 M, 처음 연료
    맵 정보
    손님 정보

필요한 변수
    end_dict : 출발지는 모두 다르기에 목적지를 딕셔너리로 담는다.
필요한 함수
    bfs

5 3 10
0 0 1 0 0
0 0 1 0 0
0 0 1 0 0
1 1 0 0 0
0 0 0 0 0
1 1
5 1 5 2
5 2 5 3
5 3 5 4

손님 못태워

5 1 10
0 0 1 0 0
0 0 1 0 0
0 0 1 0 0
1 1 0 0 0
0 0 0 0 0
1 1
1 2 5 5

3 1 10
0 0 0
0 0 0
0 0 0
1 1
1 1 3 3
내 위치가 손님위치

'''
from collections import deque

n, sonim_num, power = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
sonim_grid = [[0] * n for i in range(n)]
r, c = map(lambda x: int(x) - 1, input().split())  # 택시 위치
end_dict = {}
for s in range(sonim_num):
    sr, sc, er, ec = map(lambda x: int(x) - 1, input().split())
    end_dict[s + 1] = (er, ec)
    sonim_grid[sr][sc] = (s + 1)  # 넘버링

row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def bfs_in(tr, tc):  # 택쉬
    visited = [[False] * n for i in range(n)]
    visited[tr][tc] = True
    q = deque([(tr, tc, 0)])
    while q:
        for qs in range(len(q)):
            tr, tc, dist = q.popleft()
            if sonim_grid[tr][tc]:
                close_lst.append((dist, (tr, tc)))

            for k in range(4):
                nr = tr + row[k]
                nc = tc + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc]:
                    continue
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
        if close_lst:
            return


def bfs_out(sr, sc, er, ec):
    visited = [[False] * n for i in range(n)]
    visited[sr][sc] = True
    q = deque([(sr, sc, 0)])
    while q:
        for qs in range(len(q)):
            r, c, dist = q.popleft()
            if (r, c) == (er, ec):
                return dist
            for k in range(4):
                nr = r + row[k]
                nc = c + col[k]
                if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc] or grid[nr][nc]:
                    continue
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
    return -1


for sonim in range(sonim_num):  # 손님 수 만큼만 돌겠죵
    close_lst = []  # 가까운 손님들 담기 (거리, (좌표))
    bfs_in(r, c)
    if not close_lst:
        power = -1  # 손님 못태웠슈!!!!
        break
    close_lst.sort()
    dist, sr, sc = close_lst[0][0], close_lst[0][1][0], close_lst[0][1][1]

    power -= dist
    if power <= 0:
        power = -1  # 엥꼬낫슈
        break

    (er, ec) = end_dict[sonim_grid[sr][sc]]
    sonim_grid[sr][sc] = 0
    dist = bfs_out(sr, sc, er, ec)
    r, c = er, ec

    if dist == -1:
        power = -1  # 못데려다줫슈
        break
    power -= dist
    if power < 0:  # = 아니여도 되는지
        power = -1  # 엥꼬낫슈
        break

    power += dist * 2
print(power)
