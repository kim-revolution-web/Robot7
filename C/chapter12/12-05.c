#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
//나중에 입력할 공간입니다.

//fgets 함수의 문자열 입력 방법
int main() {

	char str[80];

	printf("공백이 포함된 문자열 입력:");
	fgets(str, sizeof(str), stdin);
	//나중에 입력할 공간입니다.
	printf("입력된 문자열은 %s 입니다.\n", str);



	return 0;
}
