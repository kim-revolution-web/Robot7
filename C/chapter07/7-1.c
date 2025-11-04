#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

/*int sum(int x, int y); */// 함수선언, 함수 헤더

// 2개의 함수로 만든 프로그램

int main() {

	int a = 10, b = 20;
	int result;
	
	result = sum(a,b);
	printf("result : %d\n", result);


	return 0;
}

int sum(int x, int y)
{
	int temp;
	temp = x + y;
	return temp;

}