'''
문제 설명
    모든점에서 가능한 depth가 4의 합들을 구해서 최댓값 갱신
    모양은 depth 4의 모든 경우의 수임
    그런데 ㅗ 모양이 돌아오는 로직이 필요
    -> 하드코딩 할거냐 vs 돌아올거냐
    -> 하드코딩..

필요한 메서드
    dfs

4 6
100 100 100 1 1 1
1 100 1 1 1 1
1 1 1 1 1 1
1 1 1 1 1 1
'''

n,m = map(int, input().split())

grid = [list(map(int, input().split())) for i in range(n)]

ans = 0

visited = [[False]*m for i in range(n)]
row = [-1,1,0,0]
col = [0,0,1,-1]
def dfs(r,c,depth,sm):
    global ans
    if depth == 4:
        ans = max(ans, sm)
        # if sm == 72:
        #     print(r,c)
        return

    for k in range(4):
        nr = r+row[k]
        nc = c+col[k]

        if not(0<=nr<n and 0<=nc<m) or visited[nr][nc]:
            continue

        visited[nr][nc] = True
        dfs(nr,nc,depth+1,sm+grid[nr][nc])
        visited[nr][nc] = False



for i in range(n):
    for j in range(m):
        visited[i][j] = True
        dfs(i,j,1,grid[i][j]) # 위치와 depth, 합
        visited[i][j] = False

# ㅏ 모양
for i in range(n-2):
    for j in range(m-1):
        ele_sum = grid[i][j]+grid[i+1][j]+grid[i+2][j]+grid[i+1][j+1]
        ans = max(ans, ele_sum)

# ㅓ 모양
for i in range(n-2):
    for j in range(1,m):
        ele_sum = grid[i][j]+grid[i+1][j]+grid[i+2][j]+grid[i+1][j-1]
        ans = max(ans, ele_sum)

# ㅜ 모양
for i in range(n-1):
    for j in range(1,m-1):
        ele_sum = grid[i][j] + grid[i][j-1] + grid[i][j+1] + grid[i + 1][j]
        ans = max(ans, ele_sum)

# ㅗ 모양
for i in range(n-1):
    for j in range(1,m-1):
        ele_sum = grid[i][j] + grid[i+1][j-1] + grid[i+1][j] + grid[i + 1][j + 1]
        ans = max(ans, ele_sum)

print(ans)