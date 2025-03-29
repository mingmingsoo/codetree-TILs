'''
문제 설명
    회전 번호/ 회전 방향이 주어졌을 때
    연쇄적으로 회전이 일어나는지 확인
    마주보는 방향이 지역이 다르면 회전 가능
                        같으면 불가능 -> 연쇄적으로 일어날 때 방향은 반대가 됨.

필요한 함수
    is_rotate() : 몇 번 의자가 회전하는지 확인
    rotate() : 위 기반 회전

필요한 변수
    rotate_arr : 회전 여부 boolean
    dir_arr : 방향 int
'''
from collections import deque

grid = [deque(map(int, input())) for i in range(4)]
order_num = int(input())


def is_rotation():
    # 내 기준 왼쪽
    left_dir = grid[idx][6]
    rd = -d
    for i in range(idx - 1, -1, -1):
        if grid[i][2] != left_dir:
            rotate_arr[i] = True
            dir_arr[i] = rd
            rd *= -1
            left_dir = grid[i][6]
        else:
            break

    # 내 기준 오른쪽
    # 내 기준 왼쪽
    light_dir = grid[idx][2]
    rd = -d
    for i in range(idx + 1, 4):
        if grid[i][6] != light_dir:
            rotate_arr[i] = True
            dir_arr[i] = rd
            rd *= -1
            light_dir = grid[i][2]
        else:
            break

def rotation():
    for i in range(4):
        if rotate_arr[i]:
            dirs = dir_arr[i]
            grid[i].rotate(dirs)

for order in range(order_num):
    idx, d = map(int, input().split())
    idx -= 1

    rotate_arr = [False] * 4
    dir_arr = [0] * 4
    rotate_arr[idx] = True
    dir_arr[idx] = d

    is_rotation()
    rotation()

ans = 0
for i in range(4):
    if grid[i][0]:
        ans += 2 ** i
print(ans)

