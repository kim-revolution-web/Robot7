//%lf 실수 표기 %le 지수 표기

#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {
	printf("%.1lf\n", 1e6);//지수 형태의 실수를 소수점 형태로 출력
	printf("%.7lf\n", 3.14e-5); // 소수점 이하 7자리까지 출력
	printf("%.7le\n", 3.14e-5);
	printf("%.7lf\n", 0.0000314);
	printf("%.7le\n", 0.0000314); // 소수점 형태의 실수를 지수 형태로 출력
	printf("%.2le\n", 0.0000314); // 지수 형태로 소수점 이하 둘째 자리까지 출력



	return 0;
}
