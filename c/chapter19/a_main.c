#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//분할 컴파일 방법 main 함수 정의
void input_data(int*, int*);
double average(int, int);

int main() {
	int a, b;
	double avg;

	input_data(&a, &b);
	avg = average(a, b);
	printf("%d와 %d의 평균 : %.1lf\n", a, b, avg);//입력값과 평균 출력

	return 0;
};
