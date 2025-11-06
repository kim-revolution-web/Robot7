#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 포인터의 선언과 사용
int main() {

	int a; //일반 변수 선언
	int* pa; // 포인터 선언

	pa = &a; //포인터에 a의 주소 대입
	*pa = 10; // 포인터로 변수 a에 10 대입

	printf("pa변수의 주소값 : %u\n", &pa);
	printf("a변수의 주소값: %u\n",&a); //  a 의 주소 값
	printf("pa변수의 주소값 : %u\n\n", pa); //가르키는 &a a의 주소값


	printf("포인터로 a값 출력 : %d\n", *pa);
	printf("변수명으로 a 값 출력: %d\n", a);


	return 0;
}
