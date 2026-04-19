#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//분할 컴파일에서 extern과 static의 용도

//main,print_data 함수 정의
int input_data();
double average();
void print_data(double);

int count = 0;
static int total = 0;

int main() {

	double avg;

	total = input_data();
	avg = average();
	print_data(avg);

	return 0;
}

void print_data(double avg)
{
	printf("입력한 양수의 개수 : %d\n", count);
	printf("전체 합과 평균 : %d, %.1lf\n", total, avg);

}