#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//정수의 합

int main() {

	int sum=0;
	for (int i = 1; i < 101; i++) {

		sum += i;
	}
	printf("%d", sum);




	return 0;
}