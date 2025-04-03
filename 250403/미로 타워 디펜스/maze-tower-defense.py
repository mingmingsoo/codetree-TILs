'''
문제 설명
    1. 공격 -> 맵 0처리 (점수 기록: 카운트 늘려주기)
    2. 0 제외 1차원 배열 변환
    3. while:
        4개이상 아닌애들만 담기
    4. 채우기

입력
    격자크기 n, 라운드 수 m
    공격 방향과 칸 수
출력
    점수 -> score = [] 배열 만들어서 한번에 계산하기

주의할 점
다 터질 때 오류 안나나? 검사하기.
7 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
0 0
이런 테케는 없지만 인덱스 에러난다.

7 1
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0
'''

n, turn = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

# location 미리 만들어 놓기
location = set()
cnt, num, two, d = 0, 1, 0, 0
r = c = n // 2

snape_row = [0, 1, 0, -1]
snape_col = [-1, 0, 1, 0]
while (r, c) != (0, 0):
    r += snape_row[d]
    c += snape_col[d]
    location.add((r, c))

    cnt += 1
    if cnt == num:
        cnt = 0
        two += 1
        d = (d + 1) % 4
    if two == 2:
        num += 1
        two = 0

r = c = n // 2
row = [0, 1, 0, -1]
col = [1, 0, -1, 0]
score = [0] * 3
for t in range(turn):
    d, p = map(int, input().split())

    for l in range(1, p + 1):
        nr = r + row[d] * l
        nc = c + col[d] * l
        if 0<=nr<n and 0<=nc<n and grid[nr][nc]:
            score[grid[nr][nc] - 1] += 1
            grid[nr][nc] = 0
    arr = []
    for sr, sc in location:
        if grid[sr][sc]:
            arr.append(grid[sr][sc])

    # 4개 이상 제거
    while True:
        arr.append(0)
        new_arr = []
        tmp = []
        same = 0
        cnt = 0
        end = True
        for num in arr:
            if num == same:
                cnt += 1
                tmp.append(num)
            elif num != same:
                if cnt <= 3:
                    new_arr.extend(tmp)
                else:
                    end = False
                    score[same - 1] += len(tmp)
                tmp = [num]
                same = num
                cnt = 1
        arr = new_arr

        if end:
            break
    # 배열 채우기
    new_arr = []
    if arr:
        arr.append(0)
        same = 0
        cnt = 0
        for num in arr:
            if num == same:
                cnt += 1
            elif num != same:
                new_arr.append(cnt)
                new_arr.append(same)
                same = num
                cnt = 1
        new_arr.pop(0)
        new_arr.pop(0)

    # 다시 이차원 배열에 넣어주기
    grid = [[0] * n for i in range(n)]
    new_arr.reverse()
    for sr, sc in location:
        if new_arr:
            grid[sr][sc] = new_arr.pop()

print(score[0] * 1 + score[1] * 2 + score[2] * 3)
