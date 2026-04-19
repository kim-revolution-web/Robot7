#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//허용되지 않는 포인터의 대입

int main() {

	int a = 10; // 변수 선언과 초기화
	int* p = &a; // 포인터 선언과 동시에 a를 가리키도록 초기화
	double* pd; // double형 변수를 가리키는 포인터

	pd = p; // 포인터 p 값을 포인터 pd에 대입
	printf("%lf\n", *pd); //pd가 가리키는 변수의 값 출력



	return 0;
}