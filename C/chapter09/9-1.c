#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//변수의 메모리 주소 확인
int main() {


	int a = 5; // int 형 변수 선언
	double b; // double 형 변수 선언
	char c; // char 형 변수 선언

	printf(" int 형 변수의 주소(10진수):%u\n", &a);
	printf(" int 형 변수의 주소(16진수):%p\n\n", &a);

	printf(" double 형 변수의 주소(10진수):%u\n", &b);
	printf(" double 형 변수의 주소(16진수):%p\n\n", &b);
	printf(" char 형 변수의 주소(10진수):%u\n", &c);
	printf(" char 형 변수의 주소(16진수):%p\n\n", &c);
	return 0;
}