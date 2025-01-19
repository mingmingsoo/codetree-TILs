package d_codeTree.미지의공간탈출;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.StringTokenizer;


/**
 * 11:55 시작
 * 16:05 종료
 * 
 * - 문제 설명
 * 1. N인 이차원 평면 위에 M인 정육면체가 세워져 있음
 * 2. 정육면체의 윗면, 동, 서, 남, 북 단면도 주어짐
 * 3. 0: 빈 공간 1: 장애물 2: 내 위치(정육면체에)
 * 	3: 정육면체 위치 4: 탈출구(정육면체 바닥에, 오직 한개)
 * 4. idx : 0 동 1 서 2 남 3 북 4 윗면
 * 
 * - 시간 이상 현상
 * 1. 미지의 공간의 바닥에는 총 F개의 시간 이상 현상
 * 	각 시간 이상 현상은 바닥의 빈 공간 (ri,ci)에서 시작하여
 * 	매 vi 의 배수 턴마다 방향 di로 한 칸씩 확산
 * 2. 시간 이상 현상은 장애물과 탈출구가 없는 빈 공간으로만 확산, 확살할 수 없으면 멈춤
 * 3. 서로 독립적이며 동시에 확산
 * 4. 시간 이상 현상이 확산된 직후 타임머신이 이동하기 때문에,
 * 	타임머신은 시간 이상 현상이 확산되는 곳으로 이동할 수 없음
 * 5. d는 동(0), 서(1), 남(2), 북(3)
 * 
 * - 출력
 * 시작점에서 탈출구까지의 최소 시간
 * 탈출할 수 없으면 -1 출력
 * 
 * - 생각해야할 점
 * 정육면체의 외부 면으로만 이동 가능함. 즉 내부 공간은 생각하지 않아도 됨.
 * 
 * - 필요한 메서드
 * 1. goBfs3() - 삼차원 배열 bfs
 * 2. goBfs2() - 이차원 배열 bfs
 * 2-1. timeError() - 시간 이상 현상 발생
 * 		
 * 
 * - 하... 오히려 로직은 해냈는데
 * 종료지점 범위 때문에 시간 많이 잡아먹음.
 * 범위에 항상 주의하자 제발!
 */

public class Main {

	static int N;
	static int M;
	static int F;

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken()); // 2차원
		M = Integer.parseInt(st.nextToken()); // 3차원
		F = Integer.parseInt(st.nextToken()); // 시간이상현상 갯수

		int startR = 0;
		int startC = 0;
		int startIdx = 0;

		int endR = 0;
		int endC = 0;
		int endIdx = 0;

		int middleR = 0;
		int middleC = 0;

		int finalR = 0;
		int finalC = 0;

		int endCubeR = 0;
		int endCubeC = 0;

		map = new int[N][N];
		cube = new int[5][M][M];

		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < N; j++) {
				map[i][j] = Integer.parseInt(st.nextToken());
				if (map[i][j] == 4) {
					finalR = i;
					finalC = j;
					map[i][j] = 0; // 목적지
				}
				if (map[i][j] == 3) {
					endCubeR = i;
					endCubeC = j;
					map[i][j] = 1; // 다시 못가게 벽으로
				}
			}
		}
		// 탈출해야할 면을 찾는 로직
		for (int i = endCubeR - M + 1; i <= endCubeR; i++) {
			for (int j = endCubeC - M + 1; j <= endCubeC; j++) {
				for (int k = 0; k < 4; k++) {
					int nr = i + row[k];
					int nc = j + col[k];
					if (nr >= 0 && nr < N && nc >= 0 && nc < N && map[nr][nc] == 0) {
						middleR = nr;
						middleC = nc;
						endR = M - 1;
						endIdx = k;
						if (k == 0) {
							endC = endCubeR - nr;
						} else if (k == 1) {
							endC = M - (endCubeR - nr) - 1;
						} else if (k == 2) {
							endC = M - (endCubeC - nc) - 1;
						} else if (k == 3) {
							endC = endCubeC - nc;
						}
						break;
					}
				}
			}
		}
		;

		for (int i = 0; i < 5; i++) {
			for (int r = 0; r < M; r++) {
				st = new StringTokenizer(br.readLine());
				for (int c = 0; c < M; c++) {
					cube[i][r][c] = Integer.parseInt(st.nextToken());
					if (cube[i][r][c] == 2) {
						startIdx = i;
						startR = r;
						startC = c;
					}
				}
			}
		}
		// 타임에 따른 배열을 이차원으로 받음.
		timeMap = new int[N][N];
		List<int[]> timeList = new ArrayList<>();
		for (int i = 0; i < F; i++) {
			st = new StringTokenizer(br.readLine());
			int r = Integer.parseInt(st.nextToken()); // 위치
			int c = Integer.parseInt(st.nextToken());
			int d = Integer.parseInt(st.nextToken()); // 방향
			int v = Integer.parseInt(st.nextToken()); // 시간
			timeList.add(new int[] { r, c, d, v });
		}
		con: for (int[] ele : timeList) {
			int r = ele[0];
			int c = ele[1];
			int d = ele[2];
			int v1 = ele[3];
			timeMap[r][c] = 1;
			for (int s = 1; s <= N; s++) {
				int v = s * v1;
				if (d == 0) {
					c++;
				} else if (d == 1) {
					c--;
				} else if (d == 2) {
					r++;
				} else if (d == 3) {
					r--;
				}
				if (r < 0 || r >= N || c < 0 || c >= N) {
					continue con;
				}
				if (r == finalR && c == finalC) {
					continue con;
				}
				if (map[r][c] == 0) {
					timeMap[r][c] = v;
				} else {
					continue con;
				}
			}
		}

//		System.out.println(startIdx + " " + startR + " " + startC);
//		System.out.println(endIdx + " " + endR + " " + endC);
//		System.out.println(middleR + " " + middleC + " " + finalR + " " + finalC);

		int ans = 0;
		ans += goBfs3(startIdx, startR, startC, endIdx, endR, endC);
		if (ans == 0) {
			System.out.println(-1);
			return;
		}
		ans++; // 한 턴 추가해주기
		int ans2 = goBfs2(middleR, middleC, finalR, finalC, ans);
		if (ans2 == 0) {
			System.out.println(-1);
			return;
		}
		System.out.println(ans2);

	}

	static int[] row = { 0, 0, 1, -1 };
	static int[] col = { 1, -1, 0, 0 };
	static int[][] map;
	static int[][][] cube;
	static int[][] timeMap;

	private static int goBfs3(int startIdx, int startR, int startC, int endIdx, int endR, int endC) {
		Queue<int[]> q = new LinkedList<>();
		boolean[][][] visited = new boolean[5][M][M];
		q.add(new int[] { startIdx, startR, startC, 0 });
		visited[startIdx][startR][startC] = true;
		while (!q.isEmpty()) {
			int[] node = q.poll();
			int idx = node[0];
			int r = node[1];
			int c = node[2];
			int time = node[3];
			if (idx == endIdx && r == endR && c == endC) {
				return time;
			}
			for (int k = 0; k < 4; k++) {
				int nr = r + row[k];
				int nc = c + col[k];
				if (idx == 4) { // 윗면일 때
					if (nr >= 0 && nr < M && nc >= 0 && nc < M) {
						if (!visited[idx][nr][nc] && cube[idx][nr][nc] == 0) {
							visited[idx][nr][nc] = true;
							q.add(new int[] { idx, nr, nc, time + 1 });
						}
					} else { // 면 이동이 필요할 때
						if (nr < 0) {
							// 북쪽으로
							nr = 0;
							nc = M - nc - 1;
						} else if (nr >= M) {
							// 남쪽으로
							nr = 0;
						} else if (nc < 0) {
							// 서쪽으로
							nc = nr;
							nr = 0;
						} else if (nc >= M) {
							// 동쪽으로
							nc = M - nr - 1;
							nr = 0;
						}
						if (!visited[k][nr][nc] && cube[k][nr][nc] == 0) {
							q.add(new int[] { k, nr, nc, time + 1 });
							visited[k][nr][nc] = true;
						}
					}
				} else { // 동서남북 면일때 -> 남쪽으로 못감
					// 면 이동 필요 없을 때.
					if (nr >= 0 && nr < M && nc >= 0 && nc < M) {
						if (!visited[idx][nr][nc] && cube[idx][nr][nc] == 0) {
							visited[idx][nr][nc] = true;
							q.add(new int[] { idx, nr, nc, time + 1 });
						}
					} else { // 면 이동이 필요할 때
						if (nr < 0) { // 윗면으로 이동
							if (idx == 0) {
								nr = nc;
								nc = 0;
							} else if (idx == 1) {
								nr = M - nc - 1;
								nc = M - 1;
							} else if (idx == 2) {
								nr = M - 1;
							} else if (idx == 3) {
								nr = 0;
								nc = M - nc - 1;
							}
							int idxNext = 4;
							if (!visited[idxNext][nr][nc] && cube[idxNext][nr][nc] == 0) {
								q.add(new int[] { idxNext, nr, nc, time + 1 });
								visited[idxNext][nr][nc] = true;
							}
						} else if (nc < 0) {
							// 왼쪽으로
							int idxNext = -1;
							if (idx == 0) {
								idxNext = 2;
								nc = M - 1;
							} else if (idx == 1) {
								idxNext = 3;
								nc = M - 1;
							} else if (idx == 2) {
								idxNext = 1;
								nc = M - 1;
							} else if (idx == 3) {
								idxNext = 0;
								nc = M - 1;
							}
							if (!visited[idxNext][nr][nc] && cube[idxNext][nr][nc] == 0) {
								q.add(new int[] { idxNext, nr, nc, time + 1 });
								visited[idxNext][nr][nc] = true;
							}
						} else if (nc >= M) {
							// 오른쪽으로
							int idxNext = -1;
							if (idx == 0) {
								idxNext = 3;
								nc = 0;
							} else if (idx == 1) {
								idxNext = 2;
								nc = 0;
							} else if (idx == 2) {
								idxNext = 0;
								nc = 0;
							} else if (idx == 3) {
								idxNext = 1;
								nc = 0;
							}
//							System.out.println(idxNext + " " + nr + " " + nc + " " + visited[idxNext][nr][nc] + " "
//									+ cube[idxNext][nr][nc]);
							if (!visited[idxNext][nr][nc] && cube[idxNext][nr][nc] == 0) {
								q.add(new int[] { idxNext, nr, nc, time + 1 });
								visited[idxNext][nr][nc] = true;
							}
						}
					}
				}
			}

		}
		return 0;
	}

	private static int goBfs2(int middleR, int middleC, int finalR, int finalC, int middleTime) {
		Queue<int[]> q = new LinkedList<>();
		boolean[][] visited = new boolean[N][N];
		q.add(new int[] { middleR, middleC, middleTime });
		visited[middleR][middleC] = true;
		while (!q.isEmpty()) {
			int[] node = q.poll();
			int r = node[0];
			int c = node[1];
			int time = node[2];
//			System.out.println(r+" "+c+" "+time);
			if (r == finalR && c == finalC) {
				return time;
			}
			for (int k = 0; k < 4; k++) {
				int nr = r + row[k];
				int nc = c + col[k];
				if (nr >= 0 && nr < N && nc >= 0 && nc < N && !visited[nr][nc] && map[nr][nc] == 0) {
					if (timeMap[nr][nc] == 0) {
						visited[nr][nc] = true;
						q.add(new int[] { nr, nc, time + 1 });
					} else if (timeMap[nr][nc] != 0 && timeMap[nr][nc] > time + 1) {
						visited[nr][nc] = true;
						q.add(new int[] { nr, nc, time + 1 });
					}
				}
			}
		}

		return 0;
	}

}