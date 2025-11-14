#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h>


int main() {

	char z[100] = {0};

	int A = 0, a = 0, n = 0, s = 0;

	printf("문자열을 입력하세요 :");
	//scanf("%s",z);
	//gets(z);
	fgets(z, strlen(z), stdin);
	z[strcmp(z,"\n")] = '\0';
	
	// for (int i = 0; i <strlen(z); i++)
	
	for (int i = 0; i <z[i] !='\0'; i++) {

		if (('A' <= z[i]) && (z[i] <= 'Z')) ++A;
		else if (('a' <= z[i]) && (z[i] <= 'z')) ++a;
		else if (('0' <= z[i]) && (z[i] <= '9')) ++n;
		else { ++s; }
	}
	
	
	printf("알파벳 대문자 %d\n", A);
	printf("알파벳 소문자 %d\n", a);
	printf("알파벳 숫자 %d\n", n);
	printf("알파벳 특수 %d\n", s);





	return 0;
}

