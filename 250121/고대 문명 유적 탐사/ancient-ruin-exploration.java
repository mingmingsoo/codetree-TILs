
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

	static class Info implements Comparable<Info> {
		int r;
		int c;
		int rotation;
		int award;

		public Info(int r, int c, int rotation, int award) {
			super();
			this.r = r;
			this.c = c;
			this.rotation = rotation;
			this.award = award;
		}

		@Override
		public int compareTo(Info o) {
			if (o.award == this.award) {
				if (this.rotation == o.rotation) {
					if (this.c == o.c) {
						return this.r - o.r;
					}
					return this.c - o.c;
				}
				return this.rotation - o.rotation;
			}
			return o.award - this.award;
		}

	}

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());

		int K = Integer.parseInt(st.nextToken()); // 반복 횟수
		int M = Integer.parseInt(st.nextToken()); // 벽면에 적힌 유물 조각 갯수 = 큐에 담을 거

		map = new int[5][5];
		for (int i = 0; i < 5; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < 5; j++) {
				map[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		numberQ = new LinkedList<>();
		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < M; i++) {
			numberQ.add(Integer.parseInt(st.nextToken()));
		}
		StringBuilder sb = new StringBuilder();
		for (int k = 0; k < K; k++) {
			ans = 0;
			List<Info> infoList = new ArrayList<>();
			// 격자 선택하는 메서드
			for (int i = 1; i <= 3; i++) {
				for (int j = 1; j <= 3; j++) {
					int[] infoArray = selectThreeMatrix(i, j);
					int rotation = infoArray[0];
					int eleAward = infoArray[1];
					infoList.add(new Info(i, j, rotation, eleAward));
				}
			}
			Collections.sort(infoList);
			Info pick = infoList.get(0);
			int r = pick.r;
			int c = pick.c;
			int ro = pick.rotation;
			int award = pick.award;
//			System.out.println(r + " " + c + " " + ro + " " + award);
			if(award == 0) {
				break;
			}
			if (ro == 1) {
				map = rotation(map, r, c);
			} else if (ro == 2) {
				map = rotation(map, r, c);
				map = rotation(map, r, c);
			} else if (ro == 3) {
				map = rotation(map, r, c);
				map = rotation(map, r, c);
				map = rotation(map, r, c);
			}
//			print(map);

			while (true) {
				int empty = makeEmpty(); // 빈 공간 생성 // 이게 반복되야 한다.
//				System.out.println("비어진 갯수:" + empty);
				ans += empty;
//				print(map);
				if (empty == 0) {
					break;
				}
				fill(); // 유물 조각 채우기
//				System.out.println("채운다!");
//				print(map);
			}


			sb.append(ans).append(" ");

		}
		System.out.println(sb);

	}

	static int ans;
	static Queue<Integer> numberQ;

	private static void print(int[][] grid) {
		System.out.println("------------");
		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[0].length; j++) {
				System.out.print(grid[i][j] + " ");
			}
			System.out.println();
		}
		System.out.println("------------");
	}

	private static int[] selectThreeMatrix(int r, int c) {

		int rotation = 1; // 회전 초기화.
		int maxAward = 0; // 회전마다 유물이 몇개 ?

		int[][] map90 = rotation(map, r, c);

		int[][] map180 = rotation(map90, r, c);

		int[][] map270 = rotation(map180, r, c);

		maxAward = getScoreBfs(map90);

		int Award180 = getScoreBfs(map180);
		if (Award180 > maxAward) {
			maxAward = Award180;
			rotation = 2; // 두번 회전했다.
		}
		int Award270 = getScoreBfs(map270);
		if (Award270 > maxAward) {
			maxAward = Award270;
			rotation = 3; // 세 번 회전했다.
		}

		return new int[] { rotation, maxAward };
	}

	private static void fill() {

		for (int j = 0; j < 5; j++) {
			for (int i = 4; i >= 0; i--) {
				if (map[i][j] == 0) {
					map[i][j] = numberQ.poll();
				}
			}
		}

	}

	private static int makeEmpty() {

		visited = new boolean[5][5];
		total = 0;
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				if (!visited[i][j]) {
					visited[i][j] = true;
					int ele = bfs(i, j, map, map[i][j]);
					if (ele >= 3) {
						delete(i, j, map[i][j]);
						total += ele;
					}
				}
			}
		}

		return total;
	}

	static int total;

	private static void delete(int r, int c, int num) {
		boolean[][] visited = new boolean[5][5];
		visited[r][c] = true;
		Queue<int[]> q = new LinkedList<>();
		q.add(new int[] { r, c });
		while (!q.isEmpty()) {
			int[] node = q.poll();
			int rr = node[0];
			int cc = node[1];
			map[rr][cc] = 0;
			for (int k = 0; k < 4; k++) {
				int nr = rr + row[k];
				int nc = cc + col[k];
				if (nr >= 0 && nr < 5 && nc >= 0 && nc < 5 && !visited[nr][nc] && map[nr][nc] == num) {
					q.add(new int[] { nr, nc });
					visited[nr][nc] = true;
				}
			}
		}

	}

	private static int getScoreBfs(int[][] grid) {
		visited = new boolean[5][5];
		int total = 0;
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				if (!visited[i][j]) {
					visited[i][j] = true;
					int ele = bfs(i, j, grid, grid[i][j]);
					if (ele >= 3) {
						total += ele;
					}
				}
			}
		}

		return total;
	}

	static boolean[][] visited;
	static int[] row = { -1, 1, 0, 0 };
	static int[] col = { 0, 0, 1, -1 };

	private static int bfs(int r, int c, int[][] grid, int num) {
		int sum = 0;
		Queue<int[]> q = new LinkedList<>();
		q.add(new int[] { r, c });
		while (!q.isEmpty()) {
			int[] node = q.poll();
			int rr = node[0];
			int cc = node[1];
			sum++;
			for (int k = 0; k < 4; k++) {
				int nr = rr + row[k];
				int nc = cc + col[k];
				if (nr >= 0 && nr < 5 && nc >= 0 && nc < 5 && !visited[nr][nc] && grid[nr][nc] == num) {
					q.add(new int[] { nr, nc });
					visited[nr][nc] = true;
				}
			}
		}
		return sum;
	}

	private static int[][] rotation(int[][] mapBefore, int r, int c) {
		int[][] rotationMap = new int[5][5];
		for (int i = 0; i < 5; i++) {
			rotationMap[i] = Arrays.copyOf(mapBefore[i], 5);
		}
		// r,c를 기준으로 시계방향 회전

		int[][] mapCopy = new int[3][3];
		for (int i = r - 1; i <= r + 1; i++) {
			for (int j = c - 1; j <= c + 1; j++) {
				mapCopy[i - r + 1][j - c + 1] = mapBefore[i][j];
			}
		}

		int[][] mapCopyRotation = new int[3][3];
		for (int i = 0; i <= 2; i++) {
			for (int j = 0; j <= 2; j++) {
				mapCopyRotation[i][j] = mapCopy[2 - j][i];
			}
		}

		for (int i = r - 1; i <= r + 1; i++) {
			for (int j = c - 1; j <= c + 1; j++) {
				rotationMap[i][j] = mapCopyRotation[i - r + 1][j - c + 1];
			}
		}

		return rotationMap;
	}

	static int[][] map;

}
