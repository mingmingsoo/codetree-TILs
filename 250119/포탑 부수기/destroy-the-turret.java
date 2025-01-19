

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.StringTokenizer;

/**
 * 문제 시작 12:30
 * - 문제 설명
 * 1. N*M 행렬 : 0인 값은 부서진 포탄
 * 2. 4가지 액션을 수행하며 K번 반복. 만약 0인 아닌 값이 1개가 된다면 중지 
 * 	-> 가장 큰 값 출력
 * 
 * - 필요한 메서드
 * 1. 공격자 선정 select
 * 		0이 아닌 가장 작은 값 선정 (값+N+M 공격력 증가)
 * 		가장 최근에 공격한 포탑이 가장 약한 포탑 - 이걸 표시해주는 행렬 필요(lastestMap)
 * 		2개 이상이면, 1. 행과 열이 가장 큰 포탑, 2. 열 값이 큰 포탑. 
 * 2. 공격자 공격 attack
 * 		자신을 제외한 가장 강한 포탑 공격
 * 		값이 가장 크고, 1. 공격한지 가장 오래된 포탑, 2. 행/열 값이 가장 작은 포탑, 3. 열이 가장 작은 포탑
 * 2-1. 공격자 공격(레이저) laserAttack(bfs)
 * 		ㄱ. 상하좌우 이동 가능
 * 		ㄴ. 0인 자리는 못지나감.
 * 		ㄷ. 이동할 때 반대편으로 이동 가능 = 행과 열을 넘어서,
 * 		ㄹ. 최단경로로 공격. 만약 없으면 bombAttack
 * 		ㅁ. 2개 이상이면 우.하.좌.상 우선 순위
 * 		ㅂ. 공격자는 공격력 만큼 줄어들고, 레이저 경로에 있는 포탑은 공격력의 절반 만큼.
 * 2-2. 공격자 공격(폭탄) bombAttack
 * 		ㄱ. 공격 대상에 8방 포탄 날림. 주변은 절반만큼 근데 공격자는 영향받지 않는다.
 * 		ㄴ. 반대편 격자에도 영향을 미침.
 * 3. 포탑 부서짐 
 * 4. 포탑 정비 restore
 * 		공격과 무관했던 포탑은 공격력 1씩 증가. - 공격여부 나타내는 boolean 배열 필요(attackedMap)
 * 
 * 
 * 
 */

public class Main {

	static class From implements Comparable<From> {
		int r;
		int c;
		int sum; // r+c
		int power; // map[r][c]
		int lastTime;

		public From(int r, int c, int sum, int power, int lastTime) {
			super();
			this.r = r;
			this.c = c;
			this.sum = sum;
			this.power = power;
			this.lastTime = lastTime;
		}

		@Override
		public String toString() {
			return "From [r=" + r + ", c=" + c + ", sum=" + sum + ", power=" + power + "]";
		}

		@Override
		public int compareTo(From o) {
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

	static class To implements Comparable<To> {
		int r;
		int c;
		int sum; // r+c
		int power; // map[r][c]
		int lastTime;

		public To(int r, int c, int sum, int power, int lastTime) {
			super();
			this.r = r;
			this.c = c;
			this.sum = sum;
			this.power = power;
			this.lastTime = lastTime;
		}

		@Override
		public String toString() {
			return "To [r=" + r + ", c=" + c + ", sum=" + sum + ", power=" + power + "]";
		}

		@Override
		public int compareTo(To o) {
			if (o.power == this.power) {
				if (o.lastTime == this.lastTime) {
					if (o.sum == this.sum) {
						return this.c - o.c;
					}
					return this.sum - o.sum;
				}
				return this.lastTime - o.lastTime; // 가장 최근(== 즉 큰 값==t)
			}

			return o.power - this.power; // 값이 가장 작은
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
			PriorityQueue<From> fromPQ = new PriorityQueue<>();
			for (int i = 0; i < N; i++) {
				for (int j = 0; j < M; j++) {
					if (map[i][j] != 0)
						fromPQ.add(new From(i, j, i + j, map[i][j], latestMap[i][j]));
				}
			}
			if (fromPQ.isEmpty()) {
				break;
			}

			// attack 과정.
			PriorityQueue<To> toPQ = new PriorityQueue<>();
			for (int i = 0; i < N; i++) {
				for (int j = 0; j < M; j++) {
					if (map[i][j] != 0)
						toPQ.add(new To(i, j, i + j, map[i][j], latestMap[i][j]));
				}
			}
			if (toPQ.isEmpty()) {
				break;
			}

			From fromNavy = fromPQ.poll();
			To toNavy = toPQ.poll();
			fromNavy.power += (N + M);
//			System.out.println("공격파워"+fromNavy.power);
			map[fromNavy.r][fromNavy.c] += (N + M);
//			System.out.println("공격파워"+map[fromNavy.r][fromNavy.c]);
			latestMap[fromNavy.r][fromNavy.c] = t;
//			System.out.println(fromNavy + " " + toNavy);

			if (laserAttack(fromNavy, toNavy, t)) {
			} else {
				bombAttack(fromNavy, toNavy);
			}

			restore();

//			print(map);
//			System.out.println("------------");
//			print(latestMap);

		}

		int ans = findMax(map);
		System.out.println(ans);
	}

	static int[] rowBomb = { -1, 1, 0, 0, 1, 1, -1, -1 };
	static int[] colBomb = { 0, 0, 1, -1, 1, -1, 1, -1 };

	private static void bombAttack(From fromNavy, To toNavy) {
		
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

	private static boolean laserAttack(From fromNavy, To toNavy, int t) {
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
//			System.out.println(r + " " + c);
			if (r == toNavy.r && c == toNavy.c) {
				tracePath(fromNavy.r, fromNavy.c, toNavy.r, toNavy.c, parentedR, parentedC, fromNavy.power / 2, t); // 레이저
																													// 지나온
																													// 애들
																													// 절반
																													// 피해
																													// 입어야함.
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
			int Powerhalf, int t) {
		// 경로 추적.
		int r = toR; // 2
		int c = toC; // 3

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
