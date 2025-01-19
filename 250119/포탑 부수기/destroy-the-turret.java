
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {

	static class Navy implements Comparable<Navy> {
		int r;
		int c;
		int sum; // r+c
		int power; // map[r][c]
		int lastTime;

		public Navy(int r, int c, int sum, int power, int lastTime) {
			super();
			this.r = r;
			this.c = c;
			this.sum = sum;
			this.power = power;
			this.lastTime = lastTime;
		}

		@Override
		public String toString() {
			return "Navy [r=" + r + ", c=" + c + ", sum=" + sum + ", power=" + power + "]";
		}

		@Override
		public int compareTo(Navy o) {
			if (o.power == this.power) {
				if (o.lastTime == this.lastTime) {
					if (o.sum == this.sum) {
						return o.c - this.c;
					}
					return o.sum - this.sum;
				}
				return o.lastTime - this.lastTime; // 가장 최근(== 즉 큰 값==t)
			}
			return this.power - o.power; // 값이 가장 작은
		}
	}

	static int N;
	static int M;
	static int[][] map;
	static int[][] latestMap;
	static boolean[][] attackedMap;

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;

		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		int T = Integer.parseInt(st.nextToken());

		map = new int[N][M];
		latestMap = new int[N][M];
		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < M; j++) {
				map[i][j] = Integer.parseInt(st.nextToken());
			}
		}

		for (int t = 1; t < T + 1; t++) {
			attackedMap = new boolean[N][M];
			// select 과정.
			List<Navy> navyList = new ArrayList<>();
			for (int i = 0; i < N; i++) {
				for (int j = 0; j < M; j++) {
					if (map[i][j] != 0)
						navyList.add(new Navy(i, j, i + j, map[i][j], latestMap[i][j]));
				}
			}
			if (navyList.isEmpty()) {
				break;
			}

			Collections.sort(navyList);
			Navy fromNavy = navyList.get(0);
			Navy toNavy = navyList.get(navyList.size()-1);
//			System.out.println(fromNavy+" -> "+ toNavy);
			if (fromNavy.r == toNavy.r && fromNavy.c == toNavy.c) {
				break; // 만약 from 과 to가 같으면 0이 아닌 값이 하나밖에 없어서 종료.
			}
			fromNavy.power += (N + M);
			map[fromNavy.r][fromNavy.c] += (N + M);
			latestMap[fromNavy.r][fromNavy.c] = t;

			if (laserAttack(fromNavy, toNavy, t)) {
			} else {
				bombAttack(fromNavy, toNavy);
			}
			restore();

		}

		int ans = findMax(map);
		System.out.println(ans);
	}

	static int[] rowBomb = { -1, 1, 0, 0, 1, 1, -1, -1 };
	static int[] colBomb = { 0, 0, 1, -1, 1, -1, 1, -1 };

	private static void bombAttack(Navy fromNavy, Navy toNavy) {

		attackedMap[fromNavy.r][fromNavy.c] = true;
		attackedMap[toNavy.r][toNavy.c] = true;
		map[toNavy.r][toNavy.c] -= fromNavy.power;
		if (map[toNavy.r][toNavy.c] < 0)
			map[toNavy.r][toNavy.c] = 0;
		for (int k = 0; k < 8; k++) {
			int nr = (toNavy.r + rowBomb[k] + N) % N;
			int nc = (toNavy.c + colBomb[k] + M) % M;
			if (nr == fromNavy.r && nc == fromNavy.c) {
				continue;
			}
			attackedMap[nr][nc] = true;
			map[nr][nc] -= fromNavy.power / 2;
			if (map[nr][nc] < 0)
				map[nr][nc] = 0;
		}

	}

	private static void restore() {
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < M; j++) {
				if (!attackedMap[i][j] && map[i][j] != 0) {
					map[i][j]++;
				}
			}
		}

	}

	static int[] row = { 0, 1, 0, -1 }; // 최단경로 우하좌상 우선순위
	static int[] col = { 1, 0, -1, 0 };

	private static boolean laserAttack(Navy fromNavy, Navy toNavy, int t) {
		Queue<int[]> q = new LinkedList<>();
		q.add(new int[] { fromNavy.r, fromNavy.c });
		boolean[][] visited = new boolean[N][M];
		visited[fromNavy.r][fromNavy.c] = true;
		int[][] parentedR = new int[N][M];
		int[][] parentedC = new int[N][M];

		for (int i = 0; i < N; i++) {
			Arrays.fill(parentedR[i], -1);
			Arrays.fill(parentedC[i], -1);
		}

		while (!q.isEmpty()) {
			int[] node = q.poll();
			int r = node[0];
			int c = node[1];
			if (r == toNavy.r && c == toNavy.c) {
				tracePath(fromNavy.r, fromNavy.c, toNavy.r, toNavy.c, parentedR, parentedC, fromNavy.power / 2); // 레이저
																													// 받은
																													// 애들은
																													// 절반만
																													// 피해
																													// 받음
				map[r][c] -= fromNavy.power; // 목적지는 그대로 피해입음.
				if (map[r][c] < 0) {
					map[r][c] = 0;
				}
				return true;
			}

			for (int k = 0; k < 4; k++) {
				int nr = (r + row[k] + N) % N;
				int nc = (c + col[k] + M) % M;

				if (!visited[nr][nc] && map[nr][nc] != 0) {
					visited[nr][nc] = true;
					q.add(new int[] { nr, nc });
					parentedR[nr][nc] = r;
					parentedC[nr][nc] = c;
				}
			}

		}

		return false;
	}

	private static void tracePath(int fromR, int fromC, int toR, int toC, int[][] parentedR, int[][] parentedC,
			int Powerhalf) {
		// 경로 추적.
		int r = toR;
		int c = toC;

		while (r != -1 && c != -1) {
			attackedMap[r][c] = true;
			if ((r != toR || c != toC) && (r != fromR || c != fromC)) {
				map[r][c] -= Powerhalf;
				if (map[r][c] < 0) {
					map[r][c] = 0;
				}
			}
			int pR = parentedR[r][c]; // 1
			int pC = parentedC[r][c]; // 3
			r = pR; // 1
			c = pC; // 3

		}

	}

	private static int findMax(int[][] map) {
		int max = 0;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < M; j++) {
				max = Math.max(max, map[i][j]);
			}
		}
		return max;
	}

	private static void print(int[][] map) {
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < M; j++) {
				System.out.print(map[i][j] + " ");
			}
			System.out.println();
		}
	}
}
