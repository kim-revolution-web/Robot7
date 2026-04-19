#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include<string.h>

// 3개의 문자열을 저장하기 위한 동적 할당
int main() {

	char temp[80];
	char* str[3];
	int i;

	for(i=0;i<3;i++)
	{
		printf("문자열을 입력하세요 :");
		fgets(temp, sizeof(temp), stdin);
		//gets(temp);
		str[i] = (char*)malloc(strlen(temp) + 1);// NULL 넣어줄려고 +1
		//str[i]= (char*)calloc(strlen(temp) +1,sizeof(char));
		strcpy(str[i], temp); //동적 할당 영역0
	}
	for (i = 0; i < 3; i++) {
		printf("%s\n", str[i]);
	}
	for (i = 0; i < 3; i++) {
		free(str[i]);//동적 할당
	}


	return 0;
}


