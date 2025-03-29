
n, length = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(n)]
gridT = map(list, zip(*grid))

ans = 0


def is_ok(row):
    idx = 0
    karo = 0
    height = row[0]

    while idx < n:
        if row[idx] == height:
            karo += 1
            idx += 1
        elif row[idx] == height + 1:  # 전보다 한 칸 높아
            if karo >= length:
                idx += 1
                height += 1
                karo = 1
            else:
                return False
        elif row[idx] == height - 1:  # 전보다 한 칸 낮아
            if idx + length >= n + 1:  # 길이가 부족하넹
                return False
            for x in range(idx, idx + length):
                if row[x] != height - 1:
                    return False
            # 여까지 왔으면 됐음
            idx += length
            karo = 0
            height -= 1
        else:
            return False

    return True


for row in grid:
    if is_ok(row):
        ans += 1

for row in gridT:
    if is_ok(row):
        ans += 1

print(ans)
