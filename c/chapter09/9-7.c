#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 포인터를 사용한 두변수의 값 교환
void swap(int* pa, int* pb);

int main() {

	int a = 10, b = 20;

	swap(&a, &b);
	printf("a:%d, b:%d\n", a, b);

	return 0;
}

void swap(int* pa, int* pb) {

	int temp;

	temp = *pa;
	*pa = *pb;
	*pb = temp;
}