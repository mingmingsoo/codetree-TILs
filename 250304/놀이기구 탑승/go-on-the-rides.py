'''
두번째 풀이
    좌표 저장해서 점수계산할 떄 3중포문 -> 1중포문으로 줄여보기
    ... 아쉽게도 시간 차이는 없네요

문제설명
    각자 선호하는 학생들이 있을 때
    우선순위에 맞춰 자리를 넣어줌.
입력
    맵크기N(학생수 ^2)
    학생들 정보
출력
    학생의 만족도
구상
    1. 처음 학생은 무조건 1,1에 넣는다.
    2. 완탐 때린다.?
        2중 포문에서
        우선순위를 계산.
'''
import heapq


n = int(input())
grid = [[0] * n for i in range(n)]
student_list = [list(map(int, input().split())) for i in range(n * n)]
row = [-1, 0, 1, 0]
col = [0, -1, 0, 1]
student_seat = [[0] * 2 for i in range(n * n)]
# 첫번째 학생
grid[1][1] = student_list[0][0]
student_list[0].append((1, 1))

for w in range(1, n * n):
    student = student_list[w][0]
    like_list = student_list[w][1:]

    q = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                continue
            like_num = 0
            empty_num = 0
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if not (0 <= nr < n and 0 <= nc < n):
                    continue
                if grid[nr][nc] in like_list:
                    # 비어있는 칸 중에서 좋아하는 학생이 인접한 칸에 가장 많은 칸으로 자리를 정한다.
                    like_num += 1
                if grid[nr][nc] == 0:
                    empty_num += 1
            heapq.heappush(q, (-like_num, -empty_num, i, j))

    like_num, empty_num, r, c = heapq.heappop(q)
    grid[r][c] = student
    student_list[w].append((r, c))
# for _ in grid:
#     print(_)
# 만족도 계산
score = 0
for i in range(n * n):
    like_list = student_list[i][1:]
    r, c = student_list[i][-1][0], student_list[i][-1][1]
    like = 0
    for k in range(4):
        nr = r + row[k]
        nc = c + col[k]
        if not (0 <= nr < n and 0 <= nc < n):
            continue
        if grid[nr][nc] in like_list:
            like += 1
    if like == 1:
        score += 1
    elif like == 2:
        score += 10
    elif like == 3:
        score += 100
    elif like == 4:
        score += 1000
print(score)
