N, limit = map(int, input().split())
arr = list(map(int, input().split()))


def rotation(small):
    n, m = len(small), len(small[0])
    ro = [[0] * n for i in range(m)]
    for i in range(m):
        for j in range(n):
            ro[i][j] = small[n - j - 1][i]
    return ro


row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]


def pull():
    plus = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if 0 <= nr < len(arr) and 0 <= nc < len(arr[nr]) and arr[nr][nc] < arr[i][j]:
                    diff = arr[i][j] - arr[nr][nc]
                    diff //= 5
                    plus.append((i, j, -diff))
                    plus.append((nr, nc, +diff))
    for r, c, diff in plus:
        arr[r][c] += diff


ans = 0
time = 0
while True:
    if max(arr) - min(arr) <= limit:
        ans = time
        break

    mini = min(arr)
    for idx, mil in enumerate(arr):
        if mil == mini:
            arr[idx] += 1

    # 일단 하나 올리기
    arr = [[arr[0]]] + [arr[1:]]
    while True:
        if len(arr) > len(arr[-1]) - len(arr[0]):
            break
        l = len(arr[0])
        small = [_[:l] for _ in arr]
        small = rotation(small)
        arr = small + [arr[-1][l:]]


    # 도우 누르기
    pull()


    # 펴기
    maxi = len(arr[-1])
    for _ in arr:
        if len(_) < maxi:
            _.extend([-1] * (maxi - len(_)))

    new_arr = []
    for j in range(maxi):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i][j] != -1:
                new_arr.append(arr[i][j])

    # 두번 반 접기
    arr = [new_arr[:N // 2][::-1]] + [new_arr[N // 2:]]
    small = [_[:N // 4] for _ in arr]
    small = rotation(small)
    small = rotation(small)
    arr = small + [_[N // 4:] for _ in arr]

    pull()

    new_arr = []
    maxi = len(arr[-1])
    for _ in arr:
        if len(_) < maxi:
            _.extend([-1] * (maxi - len(_)))

    new_arr = []
    for j in range(maxi):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i][j] != -1:
                new_arr.append(arr[i][j])
    arr = new_arr
    time += 1

print(ans)
