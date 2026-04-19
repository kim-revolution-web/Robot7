#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 배열을 처리하는 함수

void print_ary(int* pa);

int main() {

	int ary[5] = { 10,20,30,40,50 };

	print_ary(ary); //배열을 함수로 전달했다

	return 0;
}

void print_ary(int* pa) // 정수열 배열을 포인터로 할수 있다
{
	for (int i = 0; i < 5; i++) {
		printf("%d\n", pa[i]);

	}
}