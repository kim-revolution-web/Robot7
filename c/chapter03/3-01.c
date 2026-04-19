#define _CRT_RECURE_NO_WARNINGS
#include<stdio.h>

 //변수 선언 방법
int main() 
{

	int a; // int형 변수 a 선언
	int b, c; // 2개
	double da; //double 형 변수 da 선언
	char ch; // char 형 변수 ch 선언

	a = 10; //int 형 변수 a에  정수 10대입
	b = a; //int 형 변수 b에 변수 a의 값 대입
	c = a + 20; //int 형 변수c 에 변수 a의 값과 정수 20을 더합 값 대입 
	da = 3.5; //double 형 변수 da에 실수 3.5 대입
	ch = 'A'; // char 형 변수 ch에 문자 'A' 대입

	printf("변수 a의 값 : %d\n", a);
	printf("변수 b의 값 : %d\n", b);
	printf("변수 c의 값 : %d\n", c);
	printf("변수 da의 값: %.1lf\n", da);
	printf("변수의 ch의 값: %c\n", ch);



	return 0;
}
