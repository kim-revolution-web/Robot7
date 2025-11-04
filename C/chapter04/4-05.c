#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//관계연산자 결과 값 확인
int main() {

	int a = 10, b = 20, c = 10;
	int res;

	res= a > b;
	printf("a>b %d\n", res);
	res =a >= b;
	printf(" a>=b %d\n", res);
	res = a < b;
	printf("a< b :%d\n", res);
	res = (a <= b);
	printf("a<=b :%d\n", res);
	res = (a <= c);
	printf("a<=c :%d\n", res);
	res = (a == b);
	printf("a==b :%d\n", res);
	res = (a != c);
	printf("a !=b : %d\n", res);


	res = a != b;
	printf("a!=b :%d\n", res);

	a = 30;
	res = (a > 10) && (a < 20);
	printf("(a>10)&&(a<20) :%d\n", res);
	res = (a < 10) || (a > 20);
	printf("(a<10) || (a>20): %d\n", res);
	return 0;

}
