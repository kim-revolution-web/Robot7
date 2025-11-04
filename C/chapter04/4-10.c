#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//복합 대입 연산자
int main() {


	int a = 10, b = 20;
	int res = 2;


	//a = a + 20;

	a += 20; // a와 20을 더한 결과를 다시 a에 저장(+=)
	res *= b + 10;
	//b에 10을 더한 결과값에 res를 곱하고 다시 res에 저장(*=)

	printf("a= %d, b=%d\n", a, b);
	printf("res= %d\n", res);


	return 0;
}
