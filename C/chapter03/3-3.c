#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


//여러 가지 정수형 변수
int main() 
{
	short sh = 32767;  //short 형의 최댓값 초기화

	short SF = 327675; //short 형의 최댓값 넘어가면 음수 값이 나옴
	
	int in = 2147483647; // int형의 최댓값 초기화
	long ln = 2147483647; // long형의 최댔값 초기화
	long long lln = 123451234512345; // 아주 큰 값 초기화

	printf("short 형 변수 출력 : %d\n", sh);

	printf("short 형 변수 출력 : %d\n", SF);

	printf("int 형 변수 출력 :%d\n", in);
	printf("long형 변수 출력: %ld\n", ln);
	printf("long long형 변수 출력 : %lld\n", lln);// long long 형 lld 출력



	return 0;
}