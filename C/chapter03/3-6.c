#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//char 배열에 문자열 저장
int main() {


	char fruit[20] = "stawberry"; //char 배열 선언과 문자열 초기화

	printf(" 딸기 :%s\n", fruit); // 배열명으로 저장된 문자열 출력
	printf(" 딸기잼 : %s %s\n", fruit, "jam"); //문자열 상수를 %s로 출력



	return 0;

}