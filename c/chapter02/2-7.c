#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {

	/*char A[1] = "A";*/
	char A[2] = { "A" };


	//printf("%c\n", 'A'); // 문자 상수 출력
	printf("%d %d\n", A[0], A[1]);
	printf("%x %02x\n", (unsigned char)A[0], A[1]);
	//printf("%c은 %s입니다.\n", '1', "first"); //문자(%c)와 문자열(%s)을 함께 출력



	return 0;
}