#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include<string.h>

//strcat,strncat  함수를 사용한 문자열 붙이기
int main() {
	
	char str[80] = "straw";

	strcat(str, "brerry");
	printf("%s\n", str);
	strncat(str, "piece", 3);
	printf("%s\n", str);


	return 0;
}

