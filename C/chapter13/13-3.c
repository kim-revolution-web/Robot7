#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 전역 변수의 사용
void assign10();
void assign20();

int a;

int main() {
	printf("함수 호출전 a 값 : %d\n", a);

	assign10();
	assign20();

	printf("함수 호출 후 a 값 : %d\n", a);

	return 0;
}

void assign10() {
	a = 10;
}

void assign20() {
	int a;// 여기서 변수 선언을 따로 해줘서 전언변수 a랑 다르다

	a = 20;
}