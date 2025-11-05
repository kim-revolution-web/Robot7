#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {

	char str[80];

	printf("문자열 입력 :");
	//gets(str);  // 표준
	fgets(str, 80, stdin); // 최대문자수, stdin-파일 포맷
	puts("입력된 문자열 :"); 
	puts(str);  // 임배디드시 사용

	return 0;
}