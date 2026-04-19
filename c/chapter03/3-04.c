#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//unsigned 를 잘못 사용한 경우

//unsigned 자료형은 항상 양수만 저장하고 %u로 출력한다
int main() {

	unsigned int a;

	a = 4294967295; // 큰 양수 저장
	printf("%d\n", a); // %d로 출력

	a = -1; // 음수 저장
	printf("%u\n", a); //%u로 출력


	return 0;
}
