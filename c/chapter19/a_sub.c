#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//분할 컴파일 방법 input_data,average 함수 정의

void input_data(int* pa, int* pb) 
{
	printf("두 정수 입력 :");
	scanf("%d%d", pa, pb);
}

double average(int a, int b)
{
	int tot;
	double avg;

	tot = a + b;
	avg = tot / 2.0;

	return  avg;
}
