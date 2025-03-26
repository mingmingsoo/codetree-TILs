'''
문제 시작 20:41
문제 설명
    n일동안 수익 최대화
    외주 작업은 기한 t와 수익 p가 주어짐
    print(2**15) 충분
'''

n = int(input())

grid = [list(map(int, input().split())) for i in range(n)]

for idx, info in enumerate(grid):
    grid[idx].insert(0, idx)

ans = 0
sel = [0] * n


def btk(idx):
    global ans
    if idx == n:
        work = []
        for idx, flag in enumerate(sel):
            if flag:
                work.append(grid[idx])

        sumi = 0
        visited = [False] * (n + 1)
        for start, time, pay in work:
            if start + time - 1 > n:
                continue
            ok = True
            for j in range(start, start + time):
                if visited[j]:
                    ok = False
                    break
            if ok:
                for j in range(start, start + time):
                    visited[j] = True
                sumi += pay

        ans = max(ans, sumi)

        return

    sel[idx] = 0
    btk(idx + 1)
    sel[idx] = 1
    btk(idx + 1)


btk(0)
print(ans)
