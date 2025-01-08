

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Stack;
import java.util.StringTokenizer;

/**
 * 
 * 문제 시작 - 13:10
 * 
 * - 문제 설명 도로는 0, 아닌 곳은 1 집 좌표는 Sr, Sc / 공원 좌표는 Er, Ec (항상 도로 위에 있음) 도로만을 따라 최단
 * 경로로 공원까지 이동
 * 
 * M명의 전사들이 메두사를 잡고 각 전사들은 ri, ci에 위치 메두사를 향해 최단 경로로 이동 전사들은 도로/비도로 구분하지 않고 이동함.
 * 
 * * 집과 공원 초기 좌표는 다르며 전사들 또한 메두사의 집에 초기에 위치해있지 않음
 * 
 * 메두사는 전사들이 움직이기 전에 그들을 바라봄으로써 돌로 만들어 멈추게 할 수 있음.
 * 
 * - 이동 순서 1. 메두사의 이동 : 최단경로로 가되, 이동한 칸에 전사가 있으면 전사 die 여러 최단경로가 가능하면 상-하-좌-우 의
 * 순서를 따름 * 공원까지 도달하는 경로가 없을 수도 있음 2. 메두사의 시선 : 상,하,좌,우 하나의 방향을 선택해 바라봄. 90도의
 * 시야각을 가질 수 있음. 전사는 다른 전사에 의해 가려질 수 있음 - 메두사 기준 좌/ 우 나눠서 8방으로 시선에 닿는 전사들은 모두 돌로
 * 변해 움직일 수 없음 가장 많은 전사를 볼 수 있는 방향으로 봄. 만약 동이하다면 상하좌우 순서로 결정 3. 전사들의 이동 : 돌로 변하지
 * 않은 전사들은 메두사를 향해 최대 두 칸 이동. * 첫번째 이동은 메두사와 거리를 줄일 수 있는 방향으로 한 칸이동 - 상하좌우 우선순위
 * 격자 밖으로 이동 불가, 메두사의 시야에 들어오는 곳으로 이동 불가. * 두번째 이동은 메두사의 거리를 줄일 수 있는 방향으로 이동 -
 * 좌우상하 우선순위 동일하게 밖 이동 불가. 시야 이동 불가. 4. 전사의 공격 : 그렇지만 메두사는 죽지 않음.
 * 
 * -> 메두사가 공원에 도달할 때 까지 모든 전사가 이동한 거리의 합, 돌이 된 전사의 수, 메두사를 공격한 전사의 수를 출력 도착시 0
 * 출력.
 * 
 * 필요한 메서드 - medusaGoBfs : 메두사의 최단 경로 설정. 초기 한번만. * 우선순위 상하좌우 - junsaDie1 : 메두사
 * 간 곳에 전사있으면 사라짐. - medusaSea : 메두사의 시선. * 우선순위 상하좌우 - junsaMove1 : 전사 이동 *
 * 우선순위 상하좌우 - junsaMove2 : 전사 이동 * 우선순위 좌우상하 - junsaDie2 : 전사가 메두사에 도달시 사라짐.
 * 
 */

public class Main {

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken()); // 맵 크기
		M = Integer.parseInt(st.nextToken()); // 전사 수

		map = new int[N][N];

		st = new StringTokenizer(br.readLine());
		int sr = Integer.parseInt(st.nextToken()); // 메두사 시작 위치 start
		int sc = Integer.parseInt(st.nextToken());
		int er = Integer.parseInt(st.nextToken()); // 메두사 도착 위치 end
		int ec = Integer.parseInt(st.nextToken());

		junsa = new ArrayList<>();

		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < M; i++) {
			int jr = Integer.parseInt(st.nextToken());
			int jc = Integer.parseInt(st.nextToken());
			junsa.add(new int[] { jr, jc });
		}

		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < N; j++) {
				int info = Integer.parseInt(st.nextToken());
				if (info == 1) {
					map[i][j] = 1;
				}
			}
		}

		medusaGoBfs(sr, sc, er, ec);

		if (medusaStack.isEmpty()) {
			System.out.println(-1);
			return;
		}

		medusaStack.pop(); // 시작점 제거.

		while (!medusaStack.isEmpty()) {
			int[] medusa = medusaStack.pop();
			if (medusa[0] == er && medusa[1] == ec) {
				System.out.println(0);
				break;
			}

			// 출력해야할 값.
			int junsaMoveSum = 0;
			int junsaStopSum = 0;
			int junsaDealSum = 0;

			int goR = medusa[0];
			int goC = medusa[1];

//			System.out.println(goR+" "+goC);
			// 메두사가 가는 곳에 전사가 있으면 die.
			junsaDie1(goR, goC);

			// 돌이 되거라.
			junsaStopSum = medusaSea(goR, goC);

			// 돌 안된애들 이동
			junsaMoveSum = junsaMove(goR, goC);

			// 메두사 다다른 공격
			junsaDealSum = junsaDie2(goR, goC);
			System.out.println(junsaMoveSum + " " + junsaStopSum + " " + junsaDealSum);
		}
	}

	private static int junsaDie2(int r, int c) {
		int sum = 0;
		for (int i = junsa.size() - 1; i >= 0; i--) {
			if (junsa.get(i)[0] == r && junsa.get(i)[1] == c) {
				junsa.remove(i);
				sum++;
			}
		}
		return sum;
	}

	private static int junsaMove(int goR, int goC) {
		int total = 0;
		for (int i = 0; i < junsa.size(); i++) {
			if (!dollJunsa[i]) {
				// 첫번째 이동 상하좌우
				int junsaR = junsa.get(i)[0];
				int junsaC = junsa.get(i)[1];
				int distance = Math.abs(goR-junsaR) + Math.abs(goC-junsaC);
				if (junsaR == goR && junsaC == goC) {
					continue;
				}
				
				// 상하좌우 거리 다따지기.
				int distanceup = distance;
				int distancedown = distance;
				int distanceleft = distance;
				int distanceright = distance;
				int distanceAfter = distance;
				int d = 0; // 기본좌표.
				
				for(int k = 0; k<4; k++) {
					int nr = junsaR+row[k];
					int nc = junsaC+col[k];
					if(nr>=0 && nr<N && nc>=0 && nc<N) {
						if(medusaSeaMap[nr][nc]) {
							continue;
						}
						if(k ==0) {
							distanceup = Math.abs(goR-nr) + Math.abs(goC-nc);
							distanceAfter = distanceup;
						}
						else if(k==1) {
							distancedown = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distancedown<distanceAfter) {
								d = 1;
								distanceAfter = distancedown;
							}
						}
						else if(k==2) {
							distanceleft = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distanceleft<distanceAfter) {
								d =2;
								distanceAfter = distanceleft;
							}
						}
						else if(k==3) {
							distanceright = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distanceright<distanceAfter) {
								d =3;
								distanceAfter = distanceright;
							}
						}
					}
				}
				
				int after_junsaR = junsaR + row[d];
				int after_junsaC = junsaC + col[d];


				if(distanceAfter < distance) {
					total++;
					
					junsa.get(i)[0] = after_junsaR;
					junsa.get(i)[1] = after_junsaC;
				}
				else {
					continue;
				}

				// 두번째 이동 상하좌우
				junsaR = junsa.get(i)[0];
				junsaC = junsa.get(i)[1];
				distance = Math.abs(goR-junsaR) + Math.abs(goC-junsaC);
				if (junsaR == goR && junsaC == goC) {
					continue;
				}
				
				// 상하좌우 거리 다따지기.
				distanceup = distance;
				distancedown = distance;
				distanceleft = distance;
				distanceright = distance;
				distanceAfter = distance;
				d = 0; // 기본좌표.
				
				for(int k = 0; k<4; k++) {
					int nr = junsaR+row2[k];
					int nc = junsaC+col2[k];
					if(nr>=0 && nr<N && nc>=0 && nc<N) {
						if(medusaSeaMap[nr][nc]) {
							continue;
						}
						if(k ==0) {
							distanceleft = Math.abs(goR-nr) + Math.abs(goC-nc);
							distanceAfter = distanceleft;
						}
						else if(k==1) {
							distanceright = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distanceright<distanceAfter) {
								d = 1;
								distanceAfter = distanceright;
							}
						}
						else if(k==2) {
							distanceup = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distanceup<distanceAfter) {
								d =2;
								distanceAfter = distanceup;
							}
						}
						else if(k==3) {
							distancedown = Math.abs(goR-nr) + Math.abs(goC-nc);
							if(distancedown<distanceAfter) {
								d =3;
								distanceAfter = distancedown;
							}
						}
					}
				}
				
				after_junsaR = junsaR + row2[d];
				after_junsaC = junsaC + col2[d];


				if(distanceAfter < distance) {
					total++;
					
					junsa.get(i)[0] = after_junsaR;
					junsa.get(i)[1] = after_junsaC;
				}
				else {
					continue;
				}


			}
		}
		return total;
	}

	static boolean[] dollJunsa;
	static boolean[][] medusaSeaMap;

	private static int medusaSea(int goR, int goC) {
		// 메두사의 시선. * 우선순위 상하좌우
		// 몇명볼 수 있는지 체크
		// 돌이 된 전사의 수.

		int doll = 0;
		dollJunsa = new boolean[junsa.size()];

		int up = 0;
		int down = 0;
		int left = 0;
		int right = 0;

		// 위를 볼 때 계산
		boolean[][] medusaSeaMapUp = new boolean[N][N];
		for (int i = goR - 1; i >= 0; i--) {
			for (int j = goC - (goR - i); j <= goC + (goR - i); j++) {
				if (j >= 0 && j < N)
					medusaSeaMapUp[i][j] = true;
			}
		}
		// 가려지는 애들 계산
		for (int i = 0; i < junsa.size(); i++) {
			int jR = junsa.get(i)[0];
			int jC = junsa.get(i)[1];
			if (jR >= goR) {
				continue;
			}
			if (!medusaSeaMapUp[jR][jC]) {
				continue;
			}
			if (jC < goC) {
				for (int ii = jR - 1; ii >= 0; ii--) {
					for (int jj = jC - (jR - ii); jj <= jC; jj++) {
						if (jj >= 0)
							medusaSeaMapUp[ii][jj] = false;
					}
				}
			} else if (jC == goC) {
				for (int ii = jR - 1; ii >= 0; ii--) {
					medusaSeaMapUp[ii][jC] = false;
				}
			} else if (jC > goC) {
				for (int ii = jR - 1; ii >= 0; ii--) {
					for (int jj = jC; jj <= jC + (jR - ii) && jj < N; jj++) {
						if (jj >= 0)
							medusaSeaMapUp[ii][jj] = false;
					}
				}
			}
		}

		for (int i = 0; i < junsa.size(); i++) {
			if (medusaSeaMapUp[junsa.get(i)[0]][junsa.get(i)[1]]) {
				dollJunsa[i] = true;
				up++;
			}
		}
		doll = up;
		medusaSeaMap = new boolean[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				medusaSeaMap[i][j] = medusaSeaMapUp[i][j];
			}
		}

		// 아래 볼 때 계산
		boolean[][] medusaSeaMapDown = new boolean[N][N];
		for (int i = goR + 1; i < N; i++) {
			for (int j = goC - (i - goR); j <= goC + (i - goR); j++) {
				if (j >= 0 && j < N)
					medusaSeaMapDown[i][j] = true;
			}
		}
		// 가려지는 애들 계산
		for (int i = 0; i < junsa.size(); i++) {
			int jR = junsa.get(i)[0];
			int jC = junsa.get(i)[1];
			if (jR <= goR) {
				continue;
			}
			if (!medusaSeaMapDown[jR][jC]) {
				continue;
			}
			if (jC < goC) {
				for (int ii = jR + 1; ii < N; ii++) {
					for (int jj = jC - (ii - jR); jj <= jC; jj++) {
						if (jj >= 0)
							medusaSeaMapDown[ii][jj] = false;
					}
				}
			} else if (jC == goC) {
				for (int ii = jR + 1; ii < N; ii++) {
					medusaSeaMapDown[ii][jC] = false;
				}
			} else if (jC > goC) {
				for (int ii = jR + 1; ii < N; ii++) {
					for (int jj = jC; jj <= jC + (ii - jR) && jj < N; jj++) {
						if (jj >= 0)
							medusaSeaMapDown[ii][jj] = false;
					}
				}
			}
		}

		for (int i = 0; i < junsa.size(); i++) {
			if (medusaSeaMapDown[junsa.get(i)[0]][junsa.get(i)[1]]) {
				down++;
			}
		}
		if (down > doll) {
			doll = down;
			dollJunsa = new boolean[junsa.size()];
			for (int i = 0; i < junsa.size(); i++) {
				if (medusaSeaMapDown[junsa.get(i)[0]][junsa.get(i)[1]]) {
					dollJunsa[i] = true;
				}
			}

			for (int i = 0; i < N; i++) {
				for (int j = 0; j < N; j++) {
					medusaSeaMap[i][j] = medusaSeaMapDown[i][j];
				}
			}
		}

		// 왼쪽 볼 때 계산
		boolean[][] medusaSeaMapLeft = new boolean[N][N];
		for (int j = goC - 1; j >= 0; j--) {
			for (int i = goR - (goC - j); i <= goR + (goC - j); i++) {
				if (i >= 0 && i < N)
					medusaSeaMapLeft[i][j] = true;
			}
		}
		// 가려지는 애들 계산
		for (int i = 0; i < junsa.size(); i++) {
			int jR = junsa.get(i)[0];
			int jC = junsa.get(i)[1];
			if (jC >= goC) {
				continue;
			}

			if (!medusaSeaMapLeft[jR][jC]) {
				continue;
			}
			if (jR < goR) {
				for (int jj = jC - 1; jj >= 0; jj--) {
					for (int ii = jR - (jC - jj); ii <= jR; ii++) {
						if (ii >= 0)
							medusaSeaMapLeft[ii][jj] = false;
					}
				}
			} else if (jR == goR) {
				for (int jj = jC - 1; jj >= 0; jj--) {
					medusaSeaMapLeft[jR][jj] = false;
				}
			} else if (jR > goR) {
				for (int jj = jC - 1; jj >= 0; jj--) {
					for (int ii = jR; ii <= jR + (jC - jj) && ii < N; ii++) {
						if (ii >= 0)
							medusaSeaMapLeft[ii][jj] = false;
					}
				}
			}
		}

		for (int[] ele : junsa) {
			if (medusaSeaMapLeft[ele[0]][ele[1]]) {
				left++;
			}
		}

		if (left > doll) {
			doll = left;
			dollJunsa = new boolean[junsa.size()];
			for (int i = 0; i < junsa.size(); i++) {
				if (medusaSeaMapLeft[junsa.get(i)[0]][junsa.get(i)[1]]) {
					dollJunsa[i] = true;
				}
			}

			for (int i = 0; i < N; i++) {
				for (int j = 0; j < N; j++) {
					medusaSeaMap[i][j] = medusaSeaMapLeft[i][j];
				}
			}
		}

		// 오른쪽 볼 때 계산
		boolean[][] medusaSeaMapRight = new boolean[N][N];
		for (int j = goC + 1; j < N; j++) {
			for (int i = goR - (j - goC); i <= goR + (j - goC); i++) {
				if (i >= 0 && i < N)
					medusaSeaMapRight[i][j] = true;
			}
		}
		// 가려지는 애들 계산
		for (int i = 0; i < junsa.size(); i++) {
			int jR = junsa.get(i)[0];
			int jC = junsa.get(i)[1];
			if (jC <= goC) {
				continue;
			}

			if (!medusaSeaMapRight[jR][jC]) {
				continue;
			}
			if (jR < goR) {
				for (int jj = jC + 1; jj < N; jj++) {
					for (int ii = jR - (jj - jC); ii <= jR; ii++) {
						if (ii >= 0)
							medusaSeaMapRight[ii][jj] = false;
					}
				}
			} else if (jR == goR) {
				for (int jj = jC + 1; jj < N; jj++) {
					medusaSeaMapRight[jR][jj] = false;
				}
			} else if (jR > goR) {
				for (int jj = jC + 1; jj < N; jj++) {
					for (int ii = jR; ii <= jR + (jj - jC) && ii < N; ii++) {
						if (ii >= 0)
							medusaSeaMapRight[ii][jj] = false;
					}
				}
			}
		}

		for (int[] ele : junsa) {
			if (medusaSeaMapRight[ele[0]][ele[1]]) {
				right++;
			}
		}

		if (right > doll) {
			doll = right;
			dollJunsa = new boolean[junsa.size()];
			for (int i = 0; i < junsa.size(); i++) {
				if (medusaSeaMapRight[junsa.get(i)[0]][junsa.get(i)[1]]) {
					dollJunsa[i] = true;
				}
			}

			for (int i = 0; i < N; i++) {
				for (int j = 0; j < N; j++) {
					medusaSeaMap[i][j] = medusaSeaMapRight[i][j];
				}
			}
		}

		return doll;
	}

	private static void junsaDie1(int r, int c) {
		for (int i = junsa.size() - 1; i >= 0; i--) {
			if (junsa.get(i)[0] == r && junsa.get(i)[1] == c) {
				junsa.remove(i);
			}
		}

	}

	private static void print(int[][] grid) {
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				System.out.print(grid[i][j] + " ");
			}
			System.out.println();
		}
	}

	static Queue<int[]> q = new LinkedList<>();
	static Stack<int[]> medusaStack = new Stack<>();
	static List<int[]> junsa;
	static int N;
	static int M;
	static int[][] map;
	static int[] row = { -1, 1, 0, 0 }; // 상하좌우
	static int[] col = { 0, 0, -1, 1 };

	static int[] row2 = { 0, 0, -1, 1 }; // 좌우 상하
	static int[] col2 = { -1, 1, 0, 0 };

	private static void medusaGoBfs(int sr, int sc, int er, int ec) {
		// 메두사의 최단거리를 초기에 설정해줘야함.
		// q에 좌표 담을 것.
		boolean[][] visited = new boolean[N][N];
		int[][] parentR = new int[N][N];
		int[][] parentC = new int[N][N];
		for (int i = 0; i < N; i++) {
			Arrays.fill(parentR[i], -1);
			Arrays.fill(parentC[i], -1);
		}
		q.add(new int[] { sr, sc });
		visited[sr][sc] = true;

		while (!q.isEmpty()) {
			int[] node = q.poll();
			int r = node[0];
			int c = node[1];
			if (r == er && c == ec) {
				tracePath(sr, sc, er, ec, parentR, parentC);
				return;
			}
			for (int k = 0; k < 4; k++) {
				int nr = r + row[k];
				int nc = c + col[k];
				if (nr >= 0 && nr < N && nc >= 0 && nc < N && !visited[nr][nc] && map[nr][nc] != 1) {
					q.add(new int[] { nr, nc });
					visited[nr][nc] = true;
					// 부모 좌표 기록
					parentR[nr][nc] = r;
					parentC[nr][nc] = c;
				}
			}
		}
	}

	private static void tracePath(int sr, int sc, int er, int ec, int[][] parentR, int[][] parentC) {
		int r = er;
		int c = ec; // 도착지점
		while (r != -1 && c != -1) { // 시작점까지 역추적
			medusaStack.add(new int[] { r, c });
			int pr = parentR[r][c];
			int pc = parentC[r][c];
			r = pr;
			c = pc;
		}

	}

}
