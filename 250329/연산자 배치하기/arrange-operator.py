n = int(input())
lst = list(map(int, input().split()))
cal = list(map(int, input().split()))

arr = []
for idx, c in enumerate(cal):
    if c:
        arr.extend([idx] * c)
# 그리고 순열
sel = [0] * (n - 1)
visited = [False] * (n - 1)
maxi = -10**9 - 1
mini = 10**9 + 1


def perm(idx):
    global mini, maxi
    if idx == n - 1:
        num = lst[0]
        for i in range(1,n):
            c = sel[i-1]
            if c == 0:
                num += lst[i]
            elif c == 1:
                num -= lst[i]
            else:
                num *= lst[i]

        mini = min(mini, num)
        maxi = max(maxi, num)

        return

    for i in range(n - 1):
        if not visited[i]:
            visited[i] = True
            sel[idx] = arr[i]
            perm(idx + 1)
            visited[i] = False


perm(0)
print(mini, maxi)