#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main() {

	char z[100] = { 0 };
	char* str[100];
	int A = 0, a = 0, n = 0, s = 0;

	printf("문자열을 입력하세요 :");
	gets(z);

	str[100] = (char*)malloc(strlen(z + 1));
	strcpy(str[100], z);
	printf("%s\n",str[100]);

	for (int i = 0; i < 100; i++) {
		if (('A'<=str[i]) && (str[i] <= 'Z')) A++;
		else if (('a' <= str[i]) && (str[i] <= 'z')) a++;
		else if (('0' <= str[i]) && (str[i] <= '9')) n++;
		else { s++; }
	}

		printf("알파벳 대문자 %d", A);
		printf("알파벳 대문자 %d", a);
		printf("알파벳 대문자 %d", n);
		printf("알파벳 대문자 %d", s);


	free(str[0]);
	

	return 0;
};
