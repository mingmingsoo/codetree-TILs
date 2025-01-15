

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringTokenizer;
/**
 * 시작 20:00
 * 완료 22:40
 * 
 * 문제 설명
 * 1~R*1~C 행렬 
 * 정령이 골렘을 타고 내려옴
 * 
 * 골렘의 이동
 * 1. 남쪽으로 내려감
 * 2. 만약 좌,우로 남쪽으로 더 내려갈 수 있으면 회전하고 최대로 내려감.
 * 
 * 정령의 이동
 * 1. 골렘이 가장 남쪽으로 도달했으면, 정령은 가장 남쪽으로 상하좌우 인접한 칸으로 이동
 * 2. 만약 골렘의 출구가 다른 골렘하고 인접해 있으면 해당 출구를 통해 다른 골렘으로 이동해서
 * 	  정령은 가장 남쪽으로 이동
 * 3. 만약 골렘이 1번이 안돼서 정령이 도달조차 하지 못했다면 골렘 초기화.
 * 
 * 필요한 메서드
 * 1. goDown() : 아래로 최대한 내려감 -> 여기서 위치 파악해서 초기화 여부.
 * 2. isRotaion(): 회전해서 아래로 더 내려갈 수 있으면 더 내려감.
 * 3. isMove(): 정령의 이동 2번, 1번
 * 
 */
public class Main {
	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;

		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken()) + 3;
		M = Integer.parseInt(st.nextToken());
		int K = Integer.parseInt(st.nextToken()); // 정령 수

		info = new int[K][2]; // 정령 정보
		map = new int[N][M];
		for (int i = 0; i < K; i++) {
			st = new StringTokenizer(br.readLine());
			info[i][0] = Integer.parseInt(st.nextToken()) - 1;// 열
			info[i][1] = Integer.parseInt(st.nextToken()); // 위치
		}

		okpass = new boolean[N][M];
		for (int i = 0; i < K; i++) { // 정령 움직임.
			c = info[i][0]; // 열 위치
			d = info[i][1]; // 방향
			r = 1;
			// 초기 위치 확인

			// 초기 위치 설정.
			map[r][c] = (i + 1);
			for (int k = 0; k < 4; k++) {
				int nr = r + row[k];
				int nc = c + col[k];
				map[nr][nc] = (i + 1);
			}
//			System.out.println("내려가유");
			goDown(i + 1);
//			System.out.println(r + " " + c);
//			System.out.println("회전 시작!!");
			isRotation(i + 1);
			if (r <= 3) {
				map = new int[N][M];
//				System.out.println("도달못함2");
				okpass = new boolean[N][M];
				continue;
			}
			// 출구남겨주기
			wherePass(i);
//			print2(okpass);
			isMove(i);
//			System.out.println("정령번호: " + (i + 1) + " " + ans);
		}
		System.out.println(ans);
	}

	private static void wherePass(int idx) {
		if (d == 0) {
			okpass[r - 1][c] = true;
		} else if (d == 1) {
			okpass[r][c + 1] = true;
		} else if (d == 2) {
			okpass[r + 1][c] = true;
		} else {
			okpass[r][c - 1] = true;
		}
	}

	static int row[] = { 0, 0, 1, -1 };
	static int col[] = { -1, 1, 0, 0 };
	static int N;
	static int M;
	static int[][] map;
	static boolean[][] okpass;
	static int[][] info;
	static int c;
	static int d;
	static int r; // 현재 정령의 위치

	private static void goDown(int idx) {
		// 현재 중심좌표 r,c
		while (true) {
//			System.out.println();
//			print(map);
			// 중심좌표가 r+1,c일때 동남서가 비어있으면 내려갈 수 있음
			int rDown = r + 1;

			for (int k = 0; k < 3; k++) {
				int nr = rDown + row[k];
				int nc = c + col[k];
				if (nr >= N || map[nr][nc] != 0) {
					return;
				} else {
				}
			}
			r = rDown; // 중심지 변환.
			// 한칸씩 내려오기
			map[r + 1][c] = idx;
			map[r - 2][c] = 0;
			for (int j = c - 1; j <= c + 1; j++) {
				map[r][j] = idx;
				map[r - 1][j] = 0;
			}
			map[r - 1][c] = idx;
		}

	}

	private static void isRotation(int idx) {
		// d 0북 1동 2남 3서

		while (true) {
			if (r == N - 2) {
				return;
			}
			// 서쪽으로 회전이 가능하면
			if (c - 2 < 0 || r + 2 >= N) {
				break;
			}
			if (map[r - 1][c - 1] != 0|| map[r][c - 2] != 0 ||map[r + 1][c - 2] != 0 || map[r + 2][c - 1] != 0 || map[r + 1][c - 1] != 0) {
				break;
			}
			map[r + 1][c - 2] = idx;
			map[r + 2][c - 1] = idx;
			map[r + 1][c - 1] = idx;

			map[r - 1][c] = 0;
			map[r][c] = 0;
			map[r][c + 1] = 0;

			d = (d + 3) % 4;
			r++;
			c--;
//			System.out.println("왼쪽으로 회전");
//			print(map);
		}
		while (true) {
//			System.out.println("r: " + r + " N: " + N);
			if (r == N - 2) {
				return;
			}
			// 동쪽으로 회전이 가능하면
			if (c + 2 >= M || r + 2 >= N) {
				break;
			}
			if (map[r - 1][c +1] != 0||map[r][c + 2] != 0 ||map[r + 1][c + 2] != 0 || map[r + 2][c + 1] != 0 || map[r + 1][c + 1] != 0) {
				break;
			}
			map[r + 1][c + 2] = idx;
			map[r + 2][c + 1] = idx;
			map[r + 1][c + 1] = idx;

			map[r - 1][c] = 0;
			map[r][c] = 0;
			map[r][c - 1] = 0;

			d = (d + 1) % 4;
			r++;
			c++;
//			System.out.println("오른쪽으로 회전");
//			System.out.println("r: " + r + " c: " + c);
//			print(map);
		}

	}

	static int ans = 0;

	private static void isMove(int idx) {
		// 방향에 따라서 그 방향 접점이 0이 아니라면 이동 가능함.
		// bfs로
		if (r == N - 2) {
			ans += (r + 1 - 2);
			return;
		}
		boolean[][] visited = new boolean[N][M];
		Queue<int[]> q = new LinkedList<>();
		q.add(new int[] { r, c, (idx+1) }); // 원래 중심 좌표와 넘버
		visited[r][c] = true;
		int maxR = 0;
		while (!q.isEmpty()) {
			int[] node = q.poll();
			int x = node[0];
			int y = node[1];
			int num = node[2]; //2
//			System.out.println(x + ", " + y);
			if (x == N - 1) {
				ans += (x + 1 - 3);
				return;
			}
			if (x > maxR) {
				maxR = x;
			}
			for (int k = 0; k < 4; k++) {
				int nr = x + row[k];
				int nc = y + col[k];
				// 내부 골룸에선 이동 가능
				if (nr >= 0 && nr < N && nc >= 0 && nc < M && !visited[nr][nc] && map[nr][nc] == num) {
					q.add(new int[] { nr, nc, num });
					visited[nr][nc] = true;
				}
				// 외부 골룸으로 이동
				if (nr >= 0 && nr < N && nc >= 0 && nc < M && !visited[nr][nc] && map[nr][nc] != num
						&& map[nr][nc]!=0 && okpass[x][y]) {
					q.add(new int[] { nr, nc, map[nr][nc] });
					visited[nr][nc] = true;
				}
			}
		}
		ans += (maxR + 1 - 3); // 마지막 지점 도달 못하면 최대로 내려간 곳
	}

	private static void print(int[][] map) {
		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[0].length; j++) {
				System.out.print(map[i][j] + " ");
			}
			System.out.println();
		}
	}

	private static void print2(boolean[][] map) {
		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[0].length; j++) {
				if (map[i][j]) {
					System.out.print("O ");
				} else {
					System.out.print("X ");

				}
			}
			System.out.println();
		}
	}

}
