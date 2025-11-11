#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include<stdlib.h>

int main() {

	int* pi;
	int sum = 0;
	//배열을 heap에 할당해보자.
	pi = (int*)malloc(5*sizeof(int));
	printf("다섯명의 나이를 입력하세요:");

	for (int i = 0; i < 5; i++)
	{
		scanf("%d", &pi[i]);
		sum += pi[i];
	}
	printf("평균 : %.1lf\n", sum / 5.0);
	free(pi);

	return 0;
}
