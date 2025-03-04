'''
문제설명
    파이어볼은 각자의 속성이 있다.
    이동 후 두개 이상의 파이어볼이 있는 칸이라면
        1. 합쳐진다.
        2. 파이어볼은 4개로 나누어진다.
        3. 홀짝에 따라 흩어지는 위치가 다르다.
        * 질량이 0이면 소멸된다.
    k번 이동후 남아있는 질량의 합은?
입력
    맵크기 N, 파이어볼 M, 이동 횟수 move
    파이어블 r,c,m,s,d

필요한 메서드
    ele_move : 각자 움직임
    is_double : 합쳐지는거 확인, 흩뿌리기

고민되는점
    이동시 범위를 벗어나면 어떻게 되는거지?
    아 연결되어있다고 써있음

'''

n, m, move_num = map(int, input().split())
ball_list = []
for i in range(m):
    r, c, mass, s, d = map(int, input().split())
    r -= 1
    c -= 1
    ball_list.append([r, c, mass, s, d])
# print(ball_list)

row = [-1, -1, 0, 1, 1, 1, 0, -1]
col = [0, 1, 1, 1, 0, -1, -1, -1]


def ele_move():
    for i in range(len(ball_list)):
        r, c, mass, s, d = ball_list[i]
        nr = (r + row[d] * s +n) % n
        nc = (c + col[d] * s+n) % n

        ball_list[i][0] = nr
        ball_list[i][1] = nc


# 범위 확인하기 # 아마 이게 뒤에서부터 되야할거임..
def is_double():
    global ball_list
    new_ball_list = []
    isout = [False]*len(ball_list)
    for i in range(len(ball_list)-1,-1,-1):
        if isout[i]:
            continue
        r1, c1, mass1, s1, d1 = ball_list[i]
        same_idx = [(r1, c1, mass1, s1, d1, i)]
        for j in range(i - 1, -1,-1):
            r2, c2, mass2, s2, d2 = ball_list[j]
            if r1 == r2 and c1 == c2:
                same_idx.append((r2, c2, mass2, s2, d2, j))

        if (len(same_idx) > 1):
            new_mass, new_s = 0, 0
            d_list = []

            for i in range(len(same_idx)):
                r, c, mass, s, d, idx = same_idx[i]
                new_mass += mass
                new_s += s
                d_list.append(d % 2)
                isout[idx] = True
                # ball_list.pop(idx)

            new_r, new_c = same_idx[0][0], same_idx[0][1]
            new_mass //= 5
            new_s //= len(same_idx)

            if d_list.count(1) == len(same_idx) or d_list.count(0) == len(same_idx):
                new_ball_list.append([new_r, new_c, new_mass, new_s, 0])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 2])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 4])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 6])
            else:
                new_ball_list.append([new_r, new_c, new_mass, new_s, 1])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 3])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 5])
                new_ball_list.append([new_r, new_c, new_mass, new_s, 7])

    for i in  range(len(isout)):
        if not isout[i]:
            r, c, mass, s, d = ball_list[i]
            new_ball_list.append([r, c, mass, s, d])
    ball_list = new_ball_list


def is_remove():
    for i in range(len(ball_list)-1,-1,-1):
        r1, c1, mass1, s1, d1 = ball_list[i]
        if mass1 == 0:
            ball_list.pop(i)

for move in range(move_num):
    ele_move()
    is_double()
    is_remove()

ans = 0
for r, c, mass, s, d in ball_list:
    ans += mass
# print(ball_list)
print(ans)
