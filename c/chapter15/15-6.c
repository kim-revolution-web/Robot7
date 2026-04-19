#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//2차원 배열의 값을 출력하는 함수

void print_ary(int(*)[4]);

int main() {
	int ary[3][4] = { {1,2,3,4,},{5,6,7,8},{9,10,11,12} };

	print_ary(ary); // 배열명을 인수로 주고 함수 호출
	
	return 0;
}

void print_ary(int (*pa)[4]) //매개 변수는 배열 포인터
{
	int i, j;
	
	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < 4; j++)
		{
			printf("%5d", pa[i][j]);  //pa를 2차원 배열처럼 사용
		}
		printf("\n");
	}
}