#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//이중 포인터 
int swap(int** a, int** b) {

	int *temp = 0;
	temp = *a;
	*a = *b;
	*b = temp;
}


int main() {

	int a, b;
	scanf("%d %d", &a, &b);

	printf("%d %d\n", a, b);
	swap(&a, &b);

	printf("%d %d\n", a, b);

	return 0;
};