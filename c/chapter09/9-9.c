#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//포인터 없이 두 변수의 값을 바꾸는 함수 9-8에서 이어짐
//변수의 값을 인수로 주는 경우
void swap(int a,int b);

int main() {

	int a = 10, b = 20;

	swap(a,b);
	printf("a:%d, b:%d\n", a, b);

	return 0;
}

void swap(int a,int b) {

	int temp;

	temp = a;
	a = b;
	b = temp;
}