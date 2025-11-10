#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 여래 개의 1차원 배열을 2차원 배열처럼 사용
int main() {

	int ary1[4] = { 1,2,3,4 };
	int ary2[4] = { 11,12,13,14 };
	int ary3[4] = { 21,22,23,24 };
	int *pary[3] = { ary1,ary2,ary3};
	int i, j;

	for (i = 0; i < 3; i++) { //3행 반복
		for (j = 0; j < 4; j++) { // 4열 반복
			printf("%5d", pary[i][j]); //2차원 배열처럼 출력
		}
		printf("\n"); // 한 행을 출력한 후에 줄 바꿈 
	}
	//같은 표기
	printf("%5d", pary[1][2]);
	printf("%5d", *(pary[1] + 2)); //뒤에 열부터 풀어서 쓴다
	printf("%5d", *(*(pary + 1) + 2));


	return 0;
}
