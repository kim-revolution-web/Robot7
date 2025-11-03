#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//const를 사용한 변수
int main() {

	int income = 0;
	double tax;
	const double tax_rate = 0.12;

	income = 456;
	tax = income * tax_rate;
	printf("세금은 : %.1lf입니다.\n", tax);




	return 0;
}