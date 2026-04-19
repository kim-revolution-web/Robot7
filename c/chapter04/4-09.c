#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//size fo 연산자의 사용의 예
int main() {

	int a = 10;
	double b = 3.4;

	printf("int형 변수의 크기 : %d\n,", sizeof(a));
	printf("double 형 변수의 크기 :%d\n", sizeof(b));
	printf("정수형 상수의 크기:%d\n", sizeof(10));
	printf("수식의 결괏값의 크기 : %d\n", sizeof(1.5 + 3.4));

		sizeof(char)
		sizeof(short)
	return 0;

}
