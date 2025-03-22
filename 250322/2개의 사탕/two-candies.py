'''
# visited 로직도 추가하기

0322 코드트리 2개의 사탕
문제시작 19:34~ 입력받기 6분
문제설명
    상자를 상하좌우로 기울여서 빨간사탕을 빼내기
    1. 파란사탕이 나와선 안됨
    2. 동시에 나와서도 안됨
    3. 즉 빨간사탕만 나와야함
입력
    맵 정보
출력
    상자를 기울이는 최소 횟수
구상
    1. bfs로 상하좌우 움직인 것을 q에 넣어준다.
    2. 조건 검사를 파란사탕이 들어왔으면 continue 해서 그 답을 피해가게함
    3. 위치가 겹칠때 처리를 해줘야함.(누가 먼저 왔냐 따져주기)
    4. 최대 답은 10임
        즉 11이 되면 return 하기 -> 조건문 위치 중요
    5. #으로 막혀있어서 범위검사는 안해도 될듯
'''
from collections import deque

n, m = map(int, input().split())
grid = [list(input()) for i in range(n)]
red_r = red_c = blue_r = blue_c = er = ec = - 1
for i in range(1, n - 1):
    for j in range(1, m - 1):
        if grid[i][j] == "R":
            red_r, red_c = i, j
            grid[i][j] = "."
        elif grid[i][j] == "B":
            blue_r, blue_c = i, j
            grid[i][j] = "."
        elif grid[i][j] == "O":
            er, ec = i, j
            grid[i][j] = "."

ans = -1

row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]


def move(origin_r, origin_c, k):
    r, c = origin_r, origin_c
    while True:
        nr = r + row[k]
        nc = c + col[k]

        if grid[nr][nc] == "#":
            break
        r = nr
        c = nc
        if (r, c) == (er, ec):
            break

    return r, c


def bfs(srr, src, sbr, sbc):
    global ans
    q = deque([(srr, src, sbr, sbc, 0)])
    visited = set([(srr, src, sbr, sbc)])
    while q:
        red_r, red_c, blue_r, blue_c, time = q.popleft()
        if time > 10:  # 게임 종료
            return
        if (blue_r, blue_c) == (er, ec):
            continue  # 파란공 들어왔으면 넘어가기
        if (red_r, red_c) == (er, ec):
            ans = time  # 빨간공만 들어왔으면 종료
            return

        for k in range(4):
            next_red_r, next_red_c = move(red_r, red_c, k)
            next_blue_r, next_blue_c = move(blue_r, blue_c, k)

            if (next_red_r, next_red_c) == (next_blue_r, next_blue_c) and (next_red_r, next_red_c) != (er, ec):
                # 공 빠질때말고 겹쳤을 때 처리 필요
                if k == 0:  # 상
                    if blue_r < red_r:
                        next_red_r += 1
                    else:
                        next_blue_r += 1
                elif k == 1:  # 하
                    if blue_r > red_r:
                        next_red_r -= 1
                    else:
                        next_blue_r -= 1
                elif k == 2:  # 좌
                    if blue_c < red_c:
                        next_red_c += 1
                    else:
                        next_blue_c += 1
                elif k == 3:  # 우
                    if blue_c > red_c:
                        next_red_c -= 1
                    else:
                        next_blue_c -= 1
            if (red_r, red_c) == (next_red_r, next_red_c) and (blue_r, blue_c) == (next_blue_r, next_blue_c):
                continue
            else:
                if (next_red_r, next_red_c, next_blue_r, next_blue_c) not in visited:
                    visited.add((next_red_r, next_red_c, next_blue_r, next_blue_c))
                    q.append((next_red_r, next_red_c, next_blue_r, next_blue_c, time + 1))


bfs(red_r, red_c, blue_r, blue_c)
print(ans)
