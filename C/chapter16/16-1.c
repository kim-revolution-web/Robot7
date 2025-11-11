#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include<stdlib.h>

//동적 할당한 저장 공간을 사용하는 프로그램
int main() {

	int* pi;
	double* pd;
	
	pi = (int*)malloc(sizeof(int)); 
	if (pi == NULL)
	{
		printf("# 메모리가 부족합니다.\n");
		exit(1);
	}

	pd = (double*)malloc(sizeof(double));
	*pi = 10; //stack 메모리가 아닌 heap 메모리 공간에 값 삽입
	*pd = 3.4; //heap에 값 삽입

	printf("정수형으로 사용 : %d\n", *pi); // 동적 할당 영역에 저장된 값 출력
	printf("실수형으로 사용 : %.1lf\n", *pd);

	free(pi); //동적 할당 영역 반환
	free(pd);


	return 0;
}
