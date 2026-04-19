
#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int recusive(int n);

int main() {

	recusive(0);

	return 0;
}

int recusive(int n) {

	printf("number %d\n", n);

	if (n == 10)
	return 0;
	recusive(n + 1);

}
