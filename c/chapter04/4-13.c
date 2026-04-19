#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {

	int a = 10; //1010
	int b = 12; //1100

	printf("a & b: %d\n", a & b); //1000
	printf("a ^ b: %d\n", a ^ b); //0110
	printf("a | b: %d\n", a | b); //1110
	printf("~a : %d\n", ~a); //0101
	printf("a << 1 : %d\n", a << 1); //10100
	printf("a >>2 : %d\n", a >> 2 ); //0001
	

	return 0;
}