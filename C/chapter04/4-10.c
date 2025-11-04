#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {


	int a = 10, b=20;
	int res = 2;

	 
	//a = a + 20;

	a += 20;
	res *= b + 10;

	printf("a= %d, b=%d\n", a,b);
	printf("res= %d\n", res);


	return 0;
}