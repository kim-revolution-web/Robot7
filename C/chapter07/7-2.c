#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//매개 변수가 없는 함수

void myprintf();
int get_num();

int main() {

	int result;

	result = get_num();
	printf("반환값 : %d\n", result);
	
	myprintf();
	return 0;
}

int get_num() {

	int num;

	printf("양수 입력: ");
	scanf("%d", &num);

	return num;
}

void myprintf() {

	printf("Hello World~\n");
}