#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// main에 만들기
int main() {

	int a, b;
	scanf("%d %d", &a, &b);
	printf("%d %d\n", a, b);

	int temp = 0;
	temp = a;
	a = b;
	b = temp;
	
	printf("%d %d", a, b);

	return 0;
};