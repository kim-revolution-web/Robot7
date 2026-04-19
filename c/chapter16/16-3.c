#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

//calloc,realloc 함수를 사용한 양수 입력
int main() {

	int* pi;
	int size = 5;
	int count = 0;
	int num;
	int i;
	
	pi = (int*)calloc(size, sizeof(int));
	while(1)
	{
		printf("양수만 입력하세요 => ");
		scanf("%d", &num);
		if (num <= 0)break;
		if(count == size)
		{
			size += 5;
			pi = (int*)realloc(pi, size * sizeof(int));
		}
		pi[count++] = num;
	}
	for (i=0;i<count; i++)
	{
		printf("%5d", pi[i]);
	}
	free(pi);

	return 0;
}
