'''
문제 설명
    1. 도망자 이동
        new_grid 필요
        방향 검사 해서 d 바꿔주기
        술래와의 거리 확인 0 은 안됨
    2. 술래 이동
        달팽이
        방향 배열 미리 만들어두기
입력
    맵 크기 n, 도망자수 m, 나무 h, 턴 k
    도망자 좌표, 방향 -> 1:우 2:하
    나무 위치

5 3 1 100
2 4 1
1 4 2
4 2 1
2 4

9 3 1 100
1 1 1
1 9 1
9 1 2
2 4

3 3 1 100
1 1 1
1 3 1
3 1 2
2 2
'''
n, rn, tn, turn = map(int, input().split())
grid = [[[] for i in range(n)] for i in range(n)]
tree = [[0] * n for i in range(n)]
for _ in range(rn):
    rr, rc, rd = map(int, input().split())
    if rd == 1:
        grid[rr - 1][rc - 1].append(1)
    else:
        grid[rr - 1][rc - 1].append(2)
for _ in range(tn):
    tr, tc = map(int, input().split())
    tree[tr - 1][tc - 1] = 1

row = [-1, 0, 1, 0]
col = [0, 1, 0, -1]
# 술래 방향 미리 만들기
center_to_zero = [[0] * n for i in range(n)]
zero_to_center = [[0] * n for i in range(n)]
r = c = n // 2
two = cnt = d = 0
num = 1

while (r, c) != (0, 0):
    center_to_zero[r][c] = d
    r += row[d]
    c += col[d]
    zero_to_center[r][c] = (d + 2) % 4
    cnt += 1
    if cnt == num:
        d = (d + 1) % 4
        two += 1
        cnt = 0
    if two == 2:
        num += 1
        two = 0

center_to_zero[0][0] = 2


def myprint(arr):
    for i in range(n):
        for j in range(n):
            print("↑→↓←"[arr[i][j]], end=" ")
        print()


score = 0
change = 1  # 1 이면 center -> zero,-1 이면 zero -> center
r = c = n // 2
for t in range(turn):
    # 1. 도망자 이동

    new_grid = [[[] for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for rd in grid[i][j]:
                    if abs(r - i) + abs(c - j) <= 3:
                        nr = i + row[rd]
                        nc = j + col[rd]
                        if not (0 <= nr < n and 0 <= nc < n):
                            rd = (rd + 2) % 4
                        nr = i + row[rd]
                        nc = j + col[rd]
                        if (nr, nc) != (r, c):
                            new_grid[nr][nc].append(rd)
                        else:
                            new_grid[i][j].append(rd)
                    else:
                        new_grid[i][j].append(rd)

    # 2. 술래 이동
    if change == 1:
        d_grid = center_to_zero
    else:
        d_grid = zero_to_center
    d = d_grid[r][c]
    r += row[d]
    c += col[d]
    vd = d_grid[r][c]


    for l in range(3):
        nr = r + row[vd] * l
        nc = c + col[vd] * l
        if not (0 <= nr < n and 0 <= nc < n):
            break
        if new_grid[nr][nc] and not tree[nr][nc]:
            score += (t + 1) * len(new_grid[nr][nc])
            new_grid[nr][nc] = []

    if (r, c) == (0, 0) or (r, c) == (n // 2, n // 2):
        change *= -1
    grid = new_grid
print(score)
