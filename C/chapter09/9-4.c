#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 포인터에 const 사용
int main() {

	int a = 10, b = 20;
	const int* pa = &a; // 포인터 pa는 변수 a를 가르킨다.

	printf("변수 a 값: %d\n", *pa); //포인터를 간접 참조하여 a출력
	pa = &b; // 포인터가 변수 b를 가르키게 한다
	printf("변수 b의 값 : %d\n", *pa); // 포인터를 간접 참조하여 b 값 출력
	pa = &a; // 포인터가 다시 변수 a를 가리킨다.
	a = 20; // a를 직접 참조하여 값을 바꾼다.
	printf("변수 a 값 :%d\n", *pa); //포인터로 간접 참조하여 바뀐 값 출력
    //*pa= 30 (x)
	




	return 0;
}