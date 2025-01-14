

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.StringTokenizer;

/**
 * 풀이 시작 12:11
 * 풀이 종료 13:20
 */
public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());

		N = Integer.parseInt(st.nextToken()); // 맵 크기
		int M = Integer.parseInt(st.nextToken()); // 참가자 수
		int K = Integer.parseInt(st.nextToken()); // 시간제한

		map = new int[N][N];
		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < N; j++) {
				map[i][j] = Integer.parseInt(st.nextToken());
			}
		}

		runnerList = new ArrayList<>();
		for (int i = 0; i < M; i++) {
			st = new StringTokenizer(br.readLine());
			runnerList.add(new int[] { Integer.parseInt(st.nextToken()) - 1, Integer.parseInt(st.nextToken()) - 1 });
		}

		st = new StringTokenizer(br.readLine());
		exitR = Integer.parseInt(st.nextToken()) - 1;
		exitC = Integer.parseInt(st.nextToken()) - 1;
		map[exitR][exitR] = -1; // 탈출구 표시
//		System.out.println("--초기 맵--");
//		print(map);
//		System.out.println("--초기 러너 위치--");
//		for (int[] runner : runnerList) {
//			System.out.println(Arrays.toString(runner));
//		}

		totalMove = 0;

		for (int i = 0; i < K; i++) {

			run();
//			System.out.println("--이동 후 러너 위치--");
//			for (int[] runner : runnerList) {
//				System.out.println(Arrays.toString(runner));
//			}
			exit();

			if (runnerList.isEmpty()) {
				break;
			}

			squareStartR = -1;
			squareStartC = -1;
			squareLen = -1; // 변의 길이
			selectSquare();
//			System.out.println("--선택된 정사각형 정보--");
//			System.out.println("위치: (" + squareStartR + "," + squareStartC + ") , 길이: " + squareLen);
			rotation(squareStartR, squareStartC, squareLen);
//			System.out.println("--회전 후 맵--");
//			print(map);
//			System.out.println("--회전 후 러너--");
//			for (int[] runner : runnerList) {
//				System.out.println(Arrays.toString(runner));
//			}
//			System.out.println("--회전 후 탈출구");
//			System.out.println(exitR + ", " + exitC);

		}
		StringBuilder sb = new StringBuilder();
		sb.append(totalMove).append("\n").append(++exitR).append(" ").append(++exitC);
		System.out.println(sb);

	}

	static int squareStartR;
	static int squareStartC;
	static int squareLen;
	static int N;
	static int[][] map;
	static List<int[]> runnerList;
	static int exitR;
	static int exitC;
	static int totalMove;
	static int[] row = { -1, 1, 0, 0 };
	static int[] col = { 0, 0, -1, 1 };

	private static void run() {
		// 러너~탈출구 위치가 이동할 수 있는 범위에서 더 가까워지게 이동할 수 있으면 이동. 상하좌우
		con: for (int[] runner : runnerList) {
			int r = runner[0];
			int c = runner[1];

			int disOrigin = Math.abs(r - exitR) + Math.abs(c - exitC);

			for (int d = 0; d < 4; d++) {
				int nr = r + row[d];
				int nc = c + col[d];
				if (nr < 0 || nr >= N || nc < 0 || nc >= N || map[nr][nc] > 0)
					continue;
				int disNext = Math.abs(nr - exitR) + Math.abs(nc - exitC);
				if (disNext < disOrigin) {
					runner[0] = nr;
					runner[1] = nc;
					totalMove++;
					continue con;
				}
			}
		}
	}

	private static void exit() {

		for (int i = runnerList.size() - 1; i >= 0; i--) {
			int[] runner = runnerList.get(i);
			int r = runner[0];
			int c = runner[1];
			if (r == exitR && c == exitC) {
				runnerList.remove(i);
//				System.out.println("--" + i + "번 째러너 탈출--");
			}
		}
	}

	private static void selectSquare() {
		// 정사각형 길이
		outL: for (int l = 2; l <= N; l++) {
			// 시작 위치
			conI: for (int i = 0; i < N; i++) {
				if (i + l > N)
					continue outL;
				for (int j = 0; j < N; j++) {
					if (j + l > N)
						continue conI;
					if (isOk(i, j, l)) {
						squareStartR = i;
						squareStartC = j;
						squareLen = l;
						return;
					}
				}
			}
		}

	}

	private static boolean isOk(int i, int j, int l) {
		// 탈출구가 존재하고
		if (exitR >= i && exitR < i + l && exitC >= j && exitC < j + l) {
			// 한명이라도 러너가 존재하면 pick
			for (int[] runner : runnerList) {
				int r = runner[0];
				int c = runner[1];
				if (r >= i && r < i + l && c >= j && c < j + l) {
					return true;
				}
			}
		}
		return false;

	}

	private static void rotation(int squareStartR, int squareStartC, int squareLen) {
		// 1. 맵 회전 (-1씩 내구성 감소)

		// ㄱ. 절대 길이를 가지는 맵 복사본
		int[][] mapCopy = new int[squareLen][squareLen];
		for (int i = squareStartR; i < squareStartR + squareLen; i++) {
			for (int j = squareStartC; j < squareStartC + squareLen; j++) {
				mapCopy[i - squareStartR][j - squareStartC] = map[i][j];
			}
		}

		// ㄴ. 맵 복사본 회전 및 상대경로로 변환
		for (int i = 0; i < squareLen; i++) {
			for (int j = 0; j < squareLen; j++) {
				int rotatedR = squareLen - 1 - j;
				int rotatedC = i;

				if (mapCopy[rotatedR][rotatedC] > 0) {
					mapCopy[rotatedR][rotatedC]--;
				}
				map[i + squareStartR][j + squareStartC] = mapCopy[rotatedR][rotatedC];
				// 탈출구 갱신
				if (map[i + squareStartR][j + squareStartC] == -1) {
					exitR = i + squareStartR;
					exitC = j + squareStartC;
				}
			}
		}

		// 2. 사람 회전
		for (int[] runner : runnerList) {
			int r = runner[0];
			int c = runner[1];
			if (r < squareStartR || r >= squareStartR + squareLen || c < squareStartC || c >= squareStartC + squareLen)
				continue;

			// 절대 길이
			int absR = r - squareStartR;
			int absC = c - squareStartC;

			// 회전 연산
			int rotatedR = absC;
			int rotatedC = squareLen - 1 - absR;

			// 원상복구
			runner[0] = rotatedR + squareStartR;
			runner[1] = rotatedC + squareStartC;
		}

	}

	private static void print(int[][] map) {
		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map.length; j++) {
				System.out.print(map[i][j] + " ");
			}
			System.out.println();
		}
	}

}
