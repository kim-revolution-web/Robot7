#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int plus(int a, int b);
int minus(int a,int b);
double multiple(int a, int b);
double divide(int a, int b);

//plus,minus,multiple,divide
int main() {

	int x=0, y=0;
	printf("두개의 정수값을 입력하세요:");
	scanf("%d %d", &x, &y);
	int p, mi;
	double mu,di;

	p = plus(x, y);
	mi = minus(x, y);
	mu = multiple(x, y);
	di = divide(x, y);


	printf("더하기 :%d\n", p);
	printf("빼기 :%d\n", mi);
	printf("곱하기 :%.2lf\n", mu);
	printf("나누기 :%.2lf\n", di);

	return 0;
}

int plus(int a, int b) {

	return a + b;
}
int minus(int a, int b) {
	return a - b;
}
double multiple(int a, int b) {
	return (double)a * b;
}
double divide(int a, int b) {
	return (double)a / b;
}
