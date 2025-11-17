#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
//분할 컴파일에서 extern과 static의 용도

//input_data 함수 정의
extern int count;
int total = 0;

int input_data() {

	int pos;
	while (1)
	{
		printf("양수 입력:");
		scanf("%d", &pos);
		if (pos < 0)break;
		count++;
		total += pos;
	}
	return total;
}