#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//배열명 처럼 사용되는 포인터
int main() {

	int ary[3];
	int* pa = ary;
	int i;

	*pa = 10; // ary[0] 첫 번째 배열 요소에 10대입 
	*(pa + 1) = 20; // ary[1] 두 번째 배열 요소에 20 대입
	pa[2] = pa[0] + pa[1]; //  ary[3] = 10+20 대괄호를 써서 pa를 배열명 처럼 대입

	for (i = 0; i < 3; i++) {

		printf("%5d", pa[i]);
	}


	return 0;
}