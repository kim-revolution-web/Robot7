#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>

//몫과 나머지를 구하는 연산
int main() {

	double apple; //실수
	int banana; //정수
	int orange; //정수

	apple = 5.0 / 2.0; // 실수와 실수의 나누기 연산
	banana = 5 / 2; //정수와 정수의 나누기 연산
	orange = 5 % 2; //정수와 정수의 나머지 연산(%)

	printf("apple : %.1lf\n", apple);
	printf("banana : %d\n", banana);
	printf("orange : %d\n", orange);


	return 0;
}
