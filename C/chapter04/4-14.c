#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {
	
	int a = 10, b = 5;
	int res;
	res = a / b * 2;
	printf("res=%d\n", res);
	res = ++a * 3;
	printf("res = %d\n", res);
	res = a > b && a != 5;
	printf("res = %d\n", res);
	res = a % 3 == 0;
	printf("res = %d\n", res);

	return 0;
}