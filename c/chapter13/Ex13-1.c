#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int plus(int a, int b) {
	return a + b;
}
int minus(int a, int b) {
	return a - b;
}

int multiple(int a, int b) {
	return a * b;
}
double divide(int a, int b) {
	return (double)a / b;
}



int main() {

	int a = 0,b=0;
	scanf("%d %d", &a,&b);
	
	
	printf("더하기 %d\n", plus(a, b));
	printf("빼기 %d\n", minus(a, b));
	printf("곱하기 %d\n", multiple(a, b));
	printf("나누기 %.2lf\n", divide(a, b));

	return 0;
}
