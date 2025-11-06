#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h> //해더가 있어야 작동한다 , 문자열 관령 함수 원형을 모아놓은 헤더파일

//문자열을 대입하는 strcpy 함수
int main() {

	char str1[80] = "cat";
	char str2[80];

	strcpy(str1, "tiger"); // str1 배열에 "tiger" 복사
	strcpy(str2, str1); // str2 배열에 str1 배열의 문자열 복사 
	printf("%s, %s\n", str1, str2);

	return 0;

}

