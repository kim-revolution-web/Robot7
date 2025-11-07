#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>



void swap(int *a, int *b);

main() {

	int a, b;

	scanf("%d %d", &a, &b);

	swap(&a, &b);

	printf("%d %d\n", a, b);

	return 0;

}

void swap(int *a, int *b)

{
	int temp;

	temp = *a;

	*a = *b;

	*b = temp;

}