#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//유효 숫자 확인

int main() {

	float ft = 1.234567890123456789;
	double db = 1.23456789012346789;

	printf("float 형 변수의 값: %.20f\n", ft);
	printf("double 형 변수의 값 : %.20lf\n", db);

	printf("16진수 출력%02x\n", db); //unsignde int 16진수로 출력
	printf("double(hex fp): %.17a\n", db); //부동소수값을 "16진수로 출력"
	return 0;
}