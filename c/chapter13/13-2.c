#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 블록 안에 지역변수를 사용하여 두 변수를 교환하는 프로그램
int main() {

	int a = 10, b = 20;

	printf("교환 전 a 와 b의 값 : %d,%d\n", a, b);
	{//블록 시작
		int temp; //temp 변수 선언

		temp = a;
		a = b; //a와 b는 5행에 선언된 변수
		b = temp;
	}//블록 끝
	printf("교환 후 a와 b의 값 : %d, %d\n", a, b);

	return 0;
}
