#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {

	int a = 10, b = 20;
	int res;
	res = (++a, ++b); // '=' 와 ','의 우선순위 비교 = 가 높으므로 res에 ++a 값을 저장

	printf("a:%d, b:%d\n", a, b);
	printf("res:%d\n", res);

	return 0;
}