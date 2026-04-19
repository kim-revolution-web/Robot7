#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//함수 포인터를 사용한 함수 호출
int sum(int, int);

int main() {

	int(*fp)(int, int);
	int res;

	fp = sum;
	res = fp(10, 20);
	printf("result:%d\n", res);

	return 0;
}

int sum(int a, int b) {
	return (a + b);
}
