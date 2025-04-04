dice = list(map(int, input().split()))  # 이 만치 갈 수있음
#       0     1   2    3    4     5       6    7    8     9     10
adj = [[1], [2], [3], [4], [5], [6, 20], [7], [8], [9], [10], [11, 23],
#       11     12   13    14     15       16    17   18     19    20    21
       [12], [13], [14], [15], [16, 25], [17], [18], [19], [31], [21], [22],
#       22    23    24    25    26    27    28    29    30    31
       [28], [24], [28], [26], [27], [28], [29], [30], [31], [32]
       ]
score_info = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 13, 16, 19, 22, 24, 28, 27, 26,
              25, 30, 35, 40, 0]
sel = [0] * 10
ans = 0


def duple(horse,cur,where):
    for i in range(4):
        if i != horse and cur == where[i]:
            return True
    return False


def duple_perm(idx):
    global ans
    if idx == 10:
        where = [0] * 4
        score = 0
        for idx, horse in enumerate(sel):
            if where[horse] == 32:
                return # 도착칸에 있는 애를 골랐엉
            go = dice[idx]
            cur = where[horse]
            cur = adj[cur][-1]  # 일단 한 칸 이동
            where[horse] = cur
            if cur == 32:
                where[horse] = 32  # 혹시 도착 했나?
                continue
            for _ in range(go - 1):
                cur = adj[cur][0]
                if cur == 32:
                    where[horse] = 32  # 혹시 도착 했나?
                    break
            if duple(horse,cur,where):
                return
            where[horse] = cur
            score += score_info[cur]

        ans = max(ans,score)
        return

    for i in range(4):
        sel[idx] = i
        duple_perm(idx + 1)


duple_perm(0)
print(ans)