'''
m개 선택 사람들과의 거리 최소
사람들 위치는 미리 담겠다.
'''

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]

arr = []
peoples = []
for i in range(n):
    for j in range(n):
        if grid[i][j] == 2:
            arr.append((i, j))
        if grid[i][j] == 1:
            peoples.append((i, j))

sel = [0] * m
ans = int(1e9)


def combi(sidx, idx):
    global ans
    if sidx == m:
        sm = 0
        for pr, pc in peoples:
            smi = int(1e9)
            for r, c in sel:
                smi = min(abs(r - pr) + abs(c - pc), smi)
            sm += smi
        ans = min(ans, sm)

        return

    if idx == len(arr):
        return

    sel[sidx] = arr[idx]
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


combi(0, 0)
print(ans)
