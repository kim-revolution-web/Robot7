#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//여러 개의 동물 이름을 입출력하는 프로그램
int main() {

	char animal[5][20];
	char** pa;
	char* pb;
	pa = animal; // 이중 포인터
	pb = animal[1]; //단일 포인터
	int i;
	int count;

	count = sizeof(animal) / sizeof(animal[0]); // 행의 수 계산
	for (i = 0; i < count; i++) // 행의 수만큼 반복
	{
		scanf("%s", animal[i]); 
	}

	for (i = 0; i < count; i++)
	{
		printf("%s,",animal[i]); // 입력된 문자열 출력
	}

	return 0;
}
