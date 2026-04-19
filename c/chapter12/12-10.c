#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include<string.h>

//strcat,strncat  함수를 사용한 문자열 붙이기
int main() {
	
	char str[80] = "straw"; //문자열 초기화

	strcat(str, "brerry"); // str 배열에 문자열 붙이기
	printf("%s\n", str);
	strncat(str, "piece", 3); //str 배열에 3개의 문자 붙이기
	printf("%s\n", str);


	return 0;
}



