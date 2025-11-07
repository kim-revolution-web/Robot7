#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//gets 함수로 한 줄의 문자열 입력
int main() {

	char str[80];

	printf("공백이 포한된 문자열 입력:");
	//gets(str); //배열명으로 주고 함수 호출
	fgets(str, 80, stdin);
	printf("입력한 문자열은 %s 입니다.", str);


	return 0;
}