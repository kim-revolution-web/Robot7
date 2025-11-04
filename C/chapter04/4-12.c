#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//조건 연산자
int main() {

	int a = 10, b = 20, res;

	res = (a > b) ? a : b; // a와 b 중에 큰 값이 res에 저장

	printf("큰값 %d:\n", res);


	/*if (a > b) {

		res = a;
	}
	else {
		res = b;
	}

	printf("값 : %d\n", res);*/


	return 0;
}
