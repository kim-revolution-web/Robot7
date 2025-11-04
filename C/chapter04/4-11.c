#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// 콤마 연산자
int main() {

	int a = 10, b = 20;
	int res;
	res = (++a, ++b); // '=' 와 ','의 우선순위 비교 = 가 높으므로 res에 ++a 값을 저장

	printf("a:%d, b:%d\n", a, b); //차레로 연산이 수행되며 결과적으로
	printf("res:%d\n", res); // res에 저장되는 값은 증가된 b의 값이다.

	return 0;

}
