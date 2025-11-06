#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//포인터 없이 두 변수의 값을 바꾸는 함수 9-9랑 이어짐
//다른 함수의 변수 사용하기
// 선언되지 않은 식별자라 뜸
void swap();

int main() {

	int a = 10, b = 20;

	swap();
	printf("a:%d, b:%d\n", a, b);

	return 0;
}

void swap() {

	int temp;

	temp = a;
	a = b;
	b = temp;
}