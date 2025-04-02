'''
문제 설명
학생들은 무조건 비어있는 칸에 앉는데
    1. 4방 중 좋아하는 친구수가 가장 많은
    2. 비어있는 곳이 많은
    3. 행 작, 열 작
-> 첫 학생은 무조건 1,1 에 앉게된다.

입력
    격자크기n
    학생정보 (학생 번호: 좋아하는 학생들)
출력
    다 앉히고 나서 각 학생마다 4방에 인접한 친구들이 몇명이나 있나? 로 계산
'''
n = int(input())
student_info = []
link = [0] * (n * n)
for _ in range(n * n):
    tmp = list(map(int, input().split()))
    student_info.append(tmp)
    link[tmp[0] - 1] = _

grid = [[0] * n for i in range(n)]
# 첫 학생은 무조건 1,1 에 앉는다.
first = student_info[0][0]
grid[1][1] = first
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


for i in range(1, n * n):
    num, like_lst = student_info[i][0], student_info[i][1:]

    seat_lst = []
    for i in range(n):
        for j in range(n):
            if not grid[i][j]:
                like = empty = 0
                for k in range(4):
                    nr = i + row[k]
                    nc = j + col[k]
                    if not (0 <= nr < n and 0 <= nc < n):
                        continue
                    if not grid[nr][nc]:
                        empty += 1
                    if grid[nr][nc] in like_lst:
                        like += 1
                seat_lst.append((-like, empty, i, j))
    seat_lst.sort()
    _1, _2, r, c = seat_lst[0]
    grid[r][c] = num

score = 0


for i in range(n):
    for j in range(n):
        num = grid[i][j]
        idx = link[num - 1]
        like_lst = student_info[idx][1:]
        like = 0
        for k in range(4):
            nr = i + row[k]
            nc = j + col[k]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if grid[nr][nc] in like_lst:
                like += 1
        if like > 0:
            score += 10 ** (like - 1)
print(score)
