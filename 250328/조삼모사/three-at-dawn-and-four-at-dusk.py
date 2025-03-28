'''
문제 설명
    업무 n개가 주어졌을때 어떻게 반띵할래?
    아침 - 저녁 업무 강도 차이를 최소화
구상
    아침에 n//2 고르고 선택 안된 애들이 저녁!
    123/456 이랑
    456/123랑 같은뎅
    그러면 조합 하고 절반만 돌게하장.
    0123
    2301
'''

n = int(input())
grid = [list(map(int, input().split())) for i in range(n)]

sel = [0] * (n // 2)
ans = 100 * 10 + 1


def combi(sidx, idx):
    global ans
    if sel[0]:
        return
    if sidx == n // 2:
        not_sel = []
        for i in range(n):
            if i not in sel:
                not_sel.append(i)
        # print(sel, not_sel)
        A = B = 0
        for i in range(n // 2):
            for j in range(i + 1, n // 2):
                a, b, x, y = sel[i], sel[j], not_sel[i], not_sel[j]
                A += grid[a][b] + grid[b][a]
                B += grid[x][y] + grid[y][x]
        ans = min(ans,abs(A-B))
        return
    if idx == n:
        return
    sel[sidx] = idx
    combi(sidx + 1, idx + 1)
    combi(sidx, idx + 1)


combi(0, 0)
print(ans)