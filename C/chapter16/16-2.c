#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include<stdlib.h>

//동적 할당 영역을 배열처럼 사용
int main() {
	
	int* pi;
	int i, sum = 0;

	pi = (int*)malloc(5 * sizeof(int));
	if (pi ==  NULL)
	{
		printf("메모리가 부족합니다!\n");
		exit(1);
	}

	printf("다섯 명의 나이를 입력하세요:");
	for (i = 0; i < 5; i++) //i는 0부터 4까지 5번 반복
	{
		scanf("%d", &pi[i]); //배열 요소에 입력
		sum += pi[i]; //배열 요소의 값 누적
	}

	printf("다서 명의 평균 나이: %.1lf\n", (sum / 5.0));
	free(pi); //할당한 메모리 영역 반환

	return 0;
}
