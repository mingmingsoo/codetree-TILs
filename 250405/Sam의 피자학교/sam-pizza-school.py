'''
16 4
10 20 30 40 50 60 70 80 10 20 30 40 50 60 70 80

180도 회전이 내가 맘 처럼 한 것처럼 안되서 시계 2번했음 
180도 회전 확인하기

'''

n, limit = map(int, input().split())
arr = list(map(int, input().split()))
row = [-1, 1, 0, 0]
col = [0, 0, 1, -1]

def rotation(dung):
    N, M = len(dung), len(dung[0])
    new_dung = [[0] * N for i in range(M)]
    for i in range(M):
        for j in range(N):
            new_dung[i][j] = dung[N - j - 1][i]

    return new_dung


def malgi():
    plus = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            for k in range(4):
                nr = i + row[k]
                nc = j + col[k]
                if not (0 <= nr < len(arr) and 0 <= nc < len(arr[nr])) or arr[nr][nc] >= arr[i][j]:
                    continue
                diff = (arr[i][j] - arr[nr][nc]) // 5
                plus.append((i, j, -diff))
                plus.append((nr, nc, diff))

    for r, c, diff in plus:
        arr[r][c] += diff

    l = len(arr[-1])
    for _ in arr:
        if len(_) < l:
            _.extend([-1] * (l - len(_)))

    for j in range(l):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i][j] != -1:
                new_arr.append(arr[i][j])
time = 0




while True:

    if (max(arr) - min(arr)) <= limit:
        break

    time += 1
    # 1. 밀가루 뿌리기
    mini = min(arr)
    for idx, mil in enumerate(arr):
        if mil == mini:
            arr[idx] += 1

    # 2. 도우 말기
    arr = [[arr[0]]] + [arr[1:]]
    while True:
        sero = len(arr)
        namuji_karo = len(arr[-1]) - len(arr[0])
        if sero > namuji_karo:
            break

        l = len(arr[0])
        dung = [_[:l] for _ in arr]
        dung = rotation(dung)
        arr = dung + [arr[-1][l:]]

    # 3. 도우 누르기
    new_arr  = []
    malgi()
    # 4. 도우 두번 반 접기
    dung = new_arr[:n // 2]
    dung.reverse()
    new_arr = [dung] + [new_arr[n // 2:]]

    dung = [_[:n // 4] for _ in new_arr]

    dung = rotation(dung)
    dung = rotation(dung)
    new_arr = dung + [_[n // 4:] for _ in new_arr]

    arr = new_arr

    # 3. 도우 누르기
    new_arr = []
    malgi()
    arr = new_arr
print(time)