#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

//strncpy 함수를 사용한 문자열 복사 
int main() {

	char str[20] = "mango tree"; //배열 초기화

	strncpy(str, "apple-pie", 5);// "apple-pie"에서 다섯 문자만 복사

	printf("%s\n", str); // 복사 받은 문자열 출력 

	return 0;
}
