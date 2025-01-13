
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.StringTokenizer;

/**
 * 풀이 시작 16:45
 * 풀이 완료 19:40
 * 
 * - 문제 설명 M명의 참가자가 미로 탈출 미로 N*N 시작점은 1,1 칸의 3가지 상태 - 빈 칸: 참가자 이동 가능 - 벽: 참가자 이동
 * 불가 / 1~9의 내구도 / 회전할 때 내구도가 1씩 깎임 / 0이 되면 빈 칸 - 출구: 참가자가 즉시 탈출 참가자의 이동 - 1초마다
 * 한 칸씩 동시에 이동 - 최단거리는 맨해튼 거리 - 상하좌우 빈칸으로 이동 가능 - 움직인 칸은 머물렀던 칸보다 최단 거리가 가까워야함 -
 * 움직일 수 있는 칸이 두개 이상이면 상하 우선 - 움직일 수 없으면 움직이지 않음 - 한 칸에 두명 이상 있을 수 있음 미로의 회전 -
 * 참가자의 이동 후 미로가 회전 - 한 명이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡음 - 2개 이상이면 좌상단 r좌표가 작은것이
 * 우선, 그래도 작으면 c좌표가 작은 것이 우선 - 시계방향으로 90도 회전, 내구도가 1씩 깍임
 * 
 * 게임은 K초동안 반복. 모든 참가자가 시간안에 탈출하면 게임이 끝남 K초가 지나도 게임이 끝이 나지 않을 수 있음.
 * 
 * - 출력 모든 참가자들의 이동 거리 합과 출구 좌표 출력.
 * 
 * - 필요한 메서드 1. move() : 참가자들의 이동 2. pickSquare() : 가장 작은 미로 선택 3. rotaion() :
 * 미로 회전 & 내구도 감소
 * 
 * 
 */
public class Main {

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken()); // 맵 크기
		M = Integer.parseInt(st.nextToken()); // 참가자 수
		int K = Integer.parseInt(st.nextToken()); // 시간

		map = new int[N][N];
		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < N; j++) {
				map[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		peopleList = new ArrayList<>(); // 참가자 좌표

		for (int i = 0; i < M; i++) {
			st = new StringTokenizer(br.readLine());
			peopleList.add(new int[] { Integer.parseInt(st.nextToken()) - 1, Integer.parseInt(st.nextToken()) - 1 });
		}

		st = new StringTokenizer(br.readLine());
		// 탈출 정보
		exitR = Integer.parseInt(st.nextToken()) - 1;
		exitC = Integer.parseInt(st.nextToken()) - 1;
		map[exitR][exitC] = -1;

		moveTotal = 0;
		for (int k = 0; k < K; k++) {
//			System.out.println("-------" + k + "초------");
			if (peopleList.isEmpty()) {
				break;
			}
			move();

//			System.out.println("이동 후");
//			for (int[] p : peopleList) {
//				System.out.println(Arrays.toString(p));
//			}

			exit();

//			System.out.println("탈출 후");
//			for (int[] p : peopleList) {
//				System.out.println(Arrays.toString(p));
//			}

			squareR = -1;
			squareC = -1;
			squareL = -1;
			pickSquare(-1, -1, -1, exitR, exitC);
//			System.out.println("선택 후");
//			System.out.println("squareR: " + squareR + " squareC: " + squareC + " squareL: " + squareL + " exitR: "
//					+ exitR + " exitC: " + exitC);

			rotaion();
//			System.out.println("회전 후");
//			for (int i = 0; i < N; i++) {
//				for (int j = 0; j < N; j++) {
//					System.out.print(map[i][j] + " ");
//				}
//				System.out.println();
//			}
//			for (int[] p : peopleList) {
//				System.out.println(Arrays.toString(p));
//			}
		}
		StringBuilder sb = new StringBuilder();
		sb.append(moveTotal).append("\n").append(exitR+1).append(" ").append(exitC+1);
		System.out.println(sb);
	}

	private static void exit() {
		for (int i = peopleList.size() - 1; i >= 0; i--) {
			if (peopleList.get(i)[0] == exitR && peopleList.get(i)[1] == exitC) {
				peopleList.remove(i);
			}
		}

	}

	static int N;
	static int M;
	static int[][] map;
	static List<int[]> peopleList;
	static int exitR;
	static int exitC;
	static int moveTotal;
	static int[] row = { -1, 1, 0, 0 };
	static int[] col = { 0, 0, -1, 1 };
	static int squareR;
	static int squareC;
	static int squareL;

	private static void move() {
		// 참가자들의 이동
		for (int[] people : peopleList) {
			int r = people[0];
			int c = people[1];
			int distanceOrigin = Math.abs(r - exitR) + Math.abs(c - exitC); // 기존 거리
			for (int k = 0; k < 4; k++) {
				int nr = r + row[k];
				int nc = c + col[k];
				if (nr >= 0 && nr < N && nc >= 0 && nc < N && (map[nr][nc] == 0|| map[nr][nc] == -1)) {
					int distanceNext = Math.abs(nr - exitR) + Math.abs(nc - exitC);
					if (distanceNext < distanceOrigin) {
						moveTotal++;
						distanceOrigin = distanceNext;
						people[0] = nr;
						people[1] = nc;
						break;
					}
				}
			}
		}
	}

	private static void pickSquare(int r, int c, int l, int exitR, int exitC) {
		// 가장 작은 정사각형 선택
		// 좌상단이 우선이므로 0,0 에서 시작해서 사각형 크기를 늘림.. 흠 완탐 가능한가?
		con2: for (int k = 2; k < N; k++) { // 변의 길이
			con1 : for (int i = 0; i < N; i++) {
				 for (int j = 0; j < N; j++) {
					// i, j 좌표의 모든 사각형 파악.
					if(k+j >=N)
						continue con1;
					if(k+i >=N)
						continue con2;
					if (isOk(i, j, k)) {
						squareR = i;
						squareC = j;
						squareL = k;
						return;
					}
				}
			}
		}

	}

	private static boolean isOk(int i, int j, int k) { // 1 0 2
		// 사각형 안에 참가자 중 한명과 탈출만 있으면 됨

		// 탈출구가 있고
		if (exitR >= i && exitR < i + k && exitC >= j && exitC < j + k) {
			// 한명이라도 있으면 ok
			for (int[] people : peopleList) {
				int r = people[0];
				int c = people[1];
				if (r >= i && r < i + k&& c >= j && c < j + k ) {
					return true;
				} else {
					continue;
				}
			}
		} else {
			return false;
		}
		return false;
	}

	private static void rotaion() {
		// 시계 방향으로 회전
		int[][] mapCopy = new int[squareL][squareL];
		int[][] peopleMap = new int[N][N];
		int[][] peopleCopy = new int[squareL][squareL];
		int idx = 1;
		for(int[] people : peopleList) {
			peopleMap[people[0]][people[1]] = idx;
			idx++;
		}
		for (int i = squareR; i < squareR + squareL; i++) {
			for (int j = squareC; j < squareC + squareL; j++) {
				mapCopy[i - squareR][j - squareC] = map[i][j];
				peopleCopy[i - squareR][j - squareC] = peopleMap[i][j];
			}
		}
		// 멥 회전
		int[][] mapCopy2 = new int[squareL][squareL];
		int[][] peopleCopy2 = new int[squareL][squareL];
		for (int i = 0; i < squareL; i++) {
			for (int j = 0; j < squareL; j++) {
				if (mapCopy[squareL - j - 1][i] > 0) {
					mapCopy2[i][j] = mapCopy[squareL - j - 1][i] - 1;
				} else {
					mapCopy2[i][j] = mapCopy[squareL - j - 1][i];
				}
				peopleCopy2[i][j] = peopleCopy[squareL - j - 1][i];
			}
		}
		// 회전한 거 복사.
		for (int i = squareR; i < squareR + squareL; i++) {
			for (int j = squareC; j < squareC + squareL; j++) {
				map[i][j] = mapCopy2[i - squareR][j - squareC];
				peopleMap[i][j] = peopleCopy2[i - squareR][j - squareC];
				if (map[i][j] == -1) {
					exitR = i;
					exitC = j;
				}
			}
		}

		for(int i = 0; i<N ; i++) {
			for(int j = 0; j<N ; j++) {
				if(peopleMap[i][j]!=0) {
					peopleList.get(peopleMap[i][j]-1)[0] = i;
					peopleList.get(peopleMap[i][j]-1)[1] = j;
				}
			}	
		}
	}
}
