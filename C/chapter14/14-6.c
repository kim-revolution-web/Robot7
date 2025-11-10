#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//공간을 남비하지 않는다 주로 이렇게 사용
//포인터 배열로 여러 개의 문자열 출력
int main() {

	char* pary[5];//5개 짜리 배열
	int i;

	pary[0] = "dog"; 
	pary[1] = "elephant"; //*(pary+1)= "elephant"
	pary[2] = "hourse";
	pary[3] = "tiger";
	pary[4] = "lion";

	for (i = 0; i < 5; i++)
	{
		printf("%s\n", pary[i]);

	}

	return 0;
}

