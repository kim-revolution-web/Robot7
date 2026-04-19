#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int a, b, c, d;

double average(a,b,c,d) {
	
	double avg= (a + b + c + d)/4.0;
	return avg;
}


int main() {

	printf("1~100의 자연수를 입력하세요");
	scanf("%d %d %d %d", &a, &b, &c, &d);
	double v = average(a, b, c, d);
	printf("%.2lf",v );

}
