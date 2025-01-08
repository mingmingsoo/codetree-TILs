
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
 * 다시 풀기 시작 00:20
 * 다시 풀기 종료 02:21
 */
public class Main {

	public static void main(String[] args) throws IOException {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken()); // 맵 크기
		int M = Integer.parseInt(st.nextToken()); // 적 수

		// 메두사 정보
		st = new StringTokenizer(br.readLine());
		int startR = Integer.parseInt(st.nextToken());
		int startC = Integer.parseInt(st.nextToken());
		int endR = Integer.parseInt(st.nextToken());
		int endC = Integer.parseInt(st.nextToken());

		// 적 정보
		enemyList = new ArrayList<>();

		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < M; i++) {
			int enemyR = Integer.parseInt(st.nextToken());
			int enemyC = Integer.parseInt(st.nextToken());
			enemyList.add(new int[] { enemyR, enemyC });
		}

		// 맵 정보
		map = new int[N][N];
		for (int i = 0; i < N; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < N; j++) {
				int mapInfo = Integer.parseInt(st.nextToken());
				if (mapInfo == 1) {
					map[i][j] = 1;
				}
			}
		}

		// 메두사의 최단경로 구하기(우선순위: 상하좌우) - 초기에만 필요
		medusaBfs(startR, startC, endR, endC);

		medusaStack.pop(); // 시작점 제거

		// 최단경로가 없으면 -1 출력
		if (medusaStack.isEmpty()) {
			System.out.println(-1);
			return;
		}
		StringBuilder sb = new StringBuilder();
		while (!medusaStack.isEmpty()) {
			// 1. 메두사 이동
			int[] medusa = medusaStack.pop();
			// 메두사가 이동한 위치
			int medusaR = medusa[0];
			int medusaC = medusa[1];
			
			if(medusaR == endR && medusaC == endC) {
				sb.append(0);
				break;
			}

			// 메두사가 이동한 위치에 적이 있으면 소멸
			dieEnemy(medusaR, medusaC);

			// 2. 메두사의 시선 - 돌이 된 전사 수 리턴
			int enemyStopSum = medusaView(medusaR, medusaC);

			// 3. 전사들의 이동 - 전사의 이동거리 합 리턴
			int enemyMoveSum = enemyMove(medusaR, medusaC);

			// 4. 전사의 공격
			int enemyAttackSum = attackEnemy(medusaR, medusaC);
			
			sb.append(enemyMoveSum).append(" ").append(enemyStopSum).append(" ").append(enemyAttackSum).append("\n");
		}
		System.out.println(sb);

	}

	private static int enemyMove(int medusaR, int medusaC) {
		// 이동할 수 있는 전사들 체크
		int moveTotal = 0;
		for(int i = 0; i<enemyList.size();i++) {
			if(!enemyMoveNotPossible[i]) { // 움직일 수 있으면 false
				int enemyR = enemyList.get(i)[0];
				int enemyC = enemyList.get(i)[1];
				int distance = Math.abs(medusaR -  enemyR) + Math.abs(medusaC - enemyC);
				
				// 첫번째 이동 - 상하좌우 순으로
				int distanceAfter = distance;
				for(int k = 0; k<4; k++) {
					int nr = enemyR+row1[k];
					int nc = enemyC+col1[k];
					if(nr<0 || nr >=N || nc<0 || nc>=N || medusaViewMap[nr][nc]) {
						continue;
					}
					distanceAfter = Math.min(distanceAfter, Math.abs(medusaR-nr)+Math.abs(medusaC-nc));
					if(distanceAfter<distance) {
						enemyList.get(i)[0] = enemyR+row1[k];
						enemyList.get(i)[1] = enemyC+col1[k];
						break;
					}
				}
				
				if(distanceAfter>=distance) {
					continue;
				}
				
				moveTotal++; // 한번 움직임
				
				
				// 두번째 이동
				
				enemyR = enemyList.get(i)[0];
				enemyC = enemyList.get(i)[1];
				if(enemyR == medusaR && enemyC == medusaC) {
					continue;
				}
				distance = Math.abs(medusaR -  enemyR) + Math.abs(medusaC - enemyC);
				
				// 두번째 이동 - 좌우상하 순으로
				distanceAfter = distance;
				for(int k = 0; k<4; k++) {
					int nr = enemyR+row2[k];
					int nc = enemyC+col2[k];
					if(nr<0 || nr >=N || nc<0 || nc>=N || medusaViewMap[nr][nc]) {
						continue;
					}
					distanceAfter = Math.min(distanceAfter, Math.abs(medusaR-nr)+Math.abs(medusaC-nc));
					if(distanceAfter<distance) {
						enemyList.get(i)[0] = enemyR+row2[k];
						enemyList.get(i)[1] = enemyC+col2[k];
						break;
					}
				}
				
				if(distanceAfter>=distance) {
					continue;
				}
				
				moveTotal++; // 한번 움직임
			}
		}
		return moveTotal;
	}
	static boolean[] enemyMoveNotPossible;
	static boolean[][] medusaViewMap;

	private static int medusaView(int medusaR, int medusaC) {
		// 상하좌우 순으로 메두사의 시야 구하고
		// 움직일 수 있는 적들의 정보 담기.
		enemyMoveNotPossible = new boolean[enemyList.size()];
		medusaViewMap = new boolean[N][N];

		int doll = 0;
		int downDoll = 0, leftDoll = 0, rightDoll = 0;

		// 상 전체 시야
		for (int i = medusaR - 1; i >= 0; i--) {
			for (int j = medusaC - (medusaR - i); j <= medusaC + (medusaR - i); j++) {
				if (j < 0 || j >= N) {
					continue;
				}
				medusaViewMap[i][j] = true;
			}
		}
		// 상 - 가려지는 부분 찾기
		for(int[] enemy: enemyList) {
			int enemyR = enemy[0];
			int enemyC = enemy[1];
			if(enemyR >= medusaR) {
				continue;
			}
			if(!medusaViewMap[enemyR][enemyC]) {
				continue;
			}
			
			if(enemyC < medusaC) {
				for (int i = enemyR - 1; i >= 0; i--) {
					for (int j = enemyC - (enemyR - i); j <= enemyC ; j++) {
						if (j < 0 || j >= N) {
							continue;
						}
						medusaViewMap[i][j] = false;
					}
				}
			}
			else if(enemyC == medusaC) {
				for(int i = enemyR -1; i >=0; i--) {
					medusaViewMap[i][enemyC] = false;
				}
				
			} else if(enemyC > medusaC) {
				for (int i = enemyR - 1; i >= 0; i--) {
					for (int j = enemyC ; j <= enemyC + (enemyR - i); j++) {
						if (j < 0 || j >= N) {
							continue;
						}
						medusaViewMap[i][j] = false;
					}
				}
			}
			
		}
		
		for(int i = 0; i<enemyList.size();i++) {
			if(medusaViewMap[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
				doll++;
				enemyMoveNotPossible[i] = true;
			}
		}
		

		// 하 전체 시야
		boolean[][] medusaViewMapDown = new boolean[N][N];
		for (int i = medusaR + 1; i < N; i++) {
			for (int j = medusaC - (i - medusaR); j <= medusaC + (i - medusaR); j++) {
				if (j < 0 || j >= N) {
					continue;
				}
				medusaViewMapDown[i][j] = true;
			}
		}
		
		// 하 - 가려지는 부분 찾기
		for(int[] enemy: enemyList) {
			int enemyR = enemy[0];
			int enemyC = enemy[1];
			if(enemyR <= medusaR) {
				continue;
			}
			if(!medusaViewMapDown[enemyR][enemyC]) {
				continue;
			}
			
			if(enemyC < medusaC) {
				for (int i = enemyR + 1; i < N; i++) {
					for (int j = enemyC - (i - enemyR); j <= enemyC ; j++) {
						if (j < 0 || j >= N) {
							continue;
						}
						medusaViewMapDown[i][j] = false;
					}
				}
			}
			else if(enemyC == medusaC) {
				for(int i = enemyR +1; i <N; i++) {
					medusaViewMapDown[i][enemyC] = false;
				}
				
			} else if(enemyC > medusaC) {
				for (int i = enemyR + 1; i <N ; i++) {
					for (int j = enemyC ; j <= enemyC + (i - enemyR); j++) {
						if (j < 0 || j >= N) {
							continue;
						}
						medusaViewMapDown[i][j] = false;
					}
				}
			}
			
		}
		for(int i = 0; i<enemyList.size();i++) {
			if(medusaViewMapDown[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
				downDoll++;
			}
		}
		if(downDoll>doll) {
			doll = downDoll;
			Arrays.fill(enemyMoveNotPossible, false);
			
			for(int i = 0; i<N; i++) {
				for(int j = 0 ; j<N; j++) {
					medusaViewMap[i][j] = medusaViewMapDown[i][j];
				}
			}
			
			
			for(int i = 0; i<enemyList.size();i++) {
				if(medusaViewMap[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
					enemyMoveNotPossible[i] = true;
				}
			}
		}
		

		// 좌 전체 시야
		boolean[][] medusaViewMapLeft = new boolean[N][N];
		for (int j = medusaC - 1; j >= 0; j--) {
			for (int i = medusaR - (medusaC - j); i <= medusaR + (medusaC - j); i++) {
				if (i < 0 || i >= N) {
					continue;
				}
				medusaViewMapLeft[i][j] = true;
			}
		}
		
		// 좌 - 가려지는 부분 찾기
		for(int[] enemy: enemyList) {
			int enemyR = enemy[0];
			int enemyC = enemy[1];
			
			if(enemyC >= medusaC) {
				continue;
			}
			if(!medusaViewMapLeft[enemyR][enemyC]) {
				continue;
			}
			
			if(enemyR < medusaR) {
				for (int j = enemyC - 1; j >= 0; j--) {
					for (int i = enemyR - (enemyC - j); i <= enemyR ; i++) {
						if (i < 0 || i >= N) {
							continue;
						}
						medusaViewMapLeft[i][j] = false;
					}
				}
			}
			else if(enemyR == medusaR) {
				for(int j = enemyC -1; j >=0; j--) {
					medusaViewMapLeft[enemyR][j] = false;
				}
				
			} else if(enemyR > medusaR) {
				for (int j = enemyC - 1; j >= 0; j--) {
					for (int i = enemyR ; i <= enemyR + (enemyC - j); i++) {
						if (i < 0 || i >= N) {
							continue;
						}
						medusaViewMapLeft[i][j] = false;
					}
				}
			}
			
		}
		
		for(int i = 0; i<enemyList.size();i++) {
			if(medusaViewMapLeft[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
				leftDoll++;
			}
		}
		
		if(leftDoll>doll) {
			doll = leftDoll;
			
			Arrays.fill(enemyMoveNotPossible, false);
			
			for(int i = 0; i<N; i++) {
				for(int j = 0 ; j<N; j++) {
					medusaViewMap[i][j] = medusaViewMapLeft[i][j];
				}
			}
			
			
			for(int i = 0; i<enemyList.size();i++) {
				if(medusaViewMap[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
					enemyMoveNotPossible[i] = true;
				}
			}
		}
		
		
		// 우 전체 시야
		boolean[][] medusaViewMapRight = new boolean[N][N];
		for (int j = medusaC+1 ; j <N ; j++) {
			for (int i = medusaR - (j-medusaC); i <= medusaR + (j-medusaC); i++) {
				if (i < 0 || i >= N) {
					continue;
				}
				medusaViewMapRight[i][j] = true;
			}
		}
		
		// 우 - 가려지는 부분 찾기
		for(int[] enemy: enemyList) {
			int enemyR = enemy[0];
			int enemyC = enemy[1];
			
			if(enemyC <= medusaC) {
				continue;
			}
			if(!medusaViewMapRight[enemyR][enemyC]) {
				continue;
			}
			
			if(enemyR < medusaR) {
				for (int j = enemyC + 1; j <N ; j++) {
					for (int i = enemyR - (j- enemyC); i <= enemyR ; i++) {
						if (i < 0 || i >= N) {
							continue;
						}
						medusaViewMapRight[i][j] = false;
					}
				}
			}
			else if(enemyR == medusaR) {
				for(int j = enemyC +1; j <N; j++) {
					medusaViewMapRight[enemyR][j] = false;
				}
				
			} else if(enemyR > medusaR) {
				for (int j = enemyC + 1; j < N; j++) {
					for (int i = enemyR ; i <= enemyR + (j-enemyC); i++) {
						if (i < 0 || i >= N) {
							continue;
						}
						medusaViewMapRight[i][j] = false;
					}
				}
			}
		}
		for(int i = 0; i<enemyList.size();i++) {
			if(medusaViewMapRight[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
				rightDoll++;
			}
		}
		
		if(rightDoll>doll) {
			doll = rightDoll;
			
			Arrays.fill(enemyMoveNotPossible, false);
			
			for(int i = 0; i<N; i++) {
				for(int j = 0 ; j<N; j++) {
					medusaViewMap[i][j] = medusaViewMapRight[i][j];
				}
			}
			
			
			for(int i = 0; i<enemyList.size();i++) {
				if(medusaViewMap[enemyList.get(i)[0]][enemyList.get(i)[1]]) {
					enemyMoveNotPossible[i] = true;
				}
			}
		}
		return doll;
	}

	private static int attackEnemy(int medusaR, int medusaC) {
		// 전사가 메두사에 다다르면 전사 제거
		int enemyTotal = 0;
		for (int i = enemyList.size()-1; i >= 0; i--) {
			if (enemyList.get(i)[0] == medusaR && enemyList.get(i)[1] == medusaC) {
				enemyList.remove(i);
				enemyTotal++;
			}
		}
		return enemyTotal;
	}

	static List<int[]> enemyList;

	private static void dieEnemy(int medusaR, int medusaC) {
		// 메두사가 이동한 위치에 적이 있으면 제거
		for (int i = enemyList.size()-1; i >= 0; i--) {
			if (enemyList.get(i)[0] == medusaR && enemyList.get(i)[1] == medusaC) {
				enemyList.remove(i);
			}
		}
	}

	static int N;
	static int[][] map;
	// 상하좌우
	static int[] row1 = { -1, 1, 0, 0 };
	static int[] col1 = { 0, 0, -1, 1 };
	// 좌우상하
	static int[] row2 = { 0, 0, -1, 1 };
	static int[] col2 = { -1, 1, 0, 0 };

	private static void medusaBfs(int startR, int startC, int endR, int endC) {
		// 메두사 최단경로 찾기
		Queue<int[]> q = new LinkedList<>();
		boolean[][] visited = new boolean[N][N];
		q.add(new int[] { startR, startC, endR, endC });
		visited[startR][startC] = true;

		// 최단경로 좌표를 담을 parentR, parentC
		int[][] parentR = new int[N][N];
		int[][] parentC = new int[N][N];

		// 0으로 초기화 되어있으면 좌표 0이랑 겹치므로 -1로 초기화
		for (int i = 0; i < N; i++) {
			Arrays.fill(parentR[i], -1);
			Arrays.fill(parentC[i], -1);
		}
		// 시작점은 -1,-1임!! nr,nc 부터 r,c 의 정보를 담음

		while (!q.isEmpty()) {
			int[] node = q.poll();
			int r = node[0];
			int c = node[1];
			if (r == endR && c == endC) {
				pathTracking(startR, startC, endR, endC, parentR, parentC);
				return;
			}
			for (int k = 0; k < 4; k++) {
				int nr = r + row1[k];
				int nc = c + col1[k];
				if (nr >= 0 && nr < N && nc >= 0 && nc < N && !visited[nr][nc] && map[nr][nc] == 0) {
					q.add(new int[] { nr, nc });
					visited[nr][nc] = true;
					// 어디서 왔는지(부모) 좌표 기록
					parentR[nr][nc] = r;
					parentC[nr][nc] = c;
				}
			}
		}
	}

	static Stack<int[]> medusaStack;

	private static void pathTracking(int startR, int startC, int endR, int endC, int[][] parentR, int[][] parentC) {
		// 메두사 경로 추적
		medusaStack = new Stack<>();
		// 도착점 -> 끝점으로 좌표를 담을 것임.
		// main에서는 순차적으로 뽑아내야 하므로 stack으로 담음. = 후입선출
		int r = endR;
		int c = endC;

		while (r != -1 && c != -1) {
			medusaStack.add(new int[] { r, c });
			int pR = parentR[r][c]; // 부모 좌표 정보.
			int pC = parentC[r][c];
			// 좌표 갱신
			r = pR;
			c = pC;
		}

	}

}
