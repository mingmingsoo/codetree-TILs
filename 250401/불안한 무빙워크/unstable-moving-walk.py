from collections import deque

n, limit = map(int, input().split())
q = deque(map(int, input().split()))

time = 0
ans = 0


def end():
    cnt = q.count(0)
    if cnt >= limit:
        return True
    return False


people = [0] * n
while True:
    time += 1
    # 1. 무빙워크 한 칸 회전
    q.rotate(1)
    people.insert(0, people.pop())
    if people[n - 1]:
        people[n - 1] = 0

    # 2. 쩜푸
    for i in range(n - 2, -1, -1):
        if people[i] and not people[i + 1] and q[i + 1] > 0:
            people[i], people[i + 1] = people[i + 1], people[i]
            q[i + 1] -= 1
    if people[n - 1]:
        people[n - 1] = 0
    # 3. 올려!
    if not people[0] and q[0] > 0:
        people[0] = 1
        q[0] -= 1
    if people[n - 1]:
        people[n - 1] = 0
    # 4. 검증
    if end():
        ans = time
        break

print(time)
