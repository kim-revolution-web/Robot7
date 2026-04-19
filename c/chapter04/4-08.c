#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//형 변환 연산자가 필요한 경우
int main() {

	int a = 20, b = 3;
		double res;
	res = ((double)a) / ((double)b);
	printf("a=%d, b= %d\n", a, b);
	printf("a/b의 결과 : %.1lf\n", res);

	a = (int)res;
	printf("(int) %.1lf의 결과 :%d\n", res, a);

	return 0;
}

