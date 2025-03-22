n = int(input())
sonims = list(map(int, input().split()))
boss, manager = map(int, input().split())
for i in range(n):
    sonims[i] -= boss
    if sonims[i] < 0:
        sonims[i] = 0
ans = n

for i in range(n):
    mok = sonims[i] // manager
    mod = sonims[i] % manager
    if mod == 0:
        ans += mok
    else:
        ans += mok + 1
print(ans)
