#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//빈칸을 포함한 문자열 입력
int main() {

	char str[80];

	printf("문자열 입력 :"); // 입력 안내 메시지 출력
	//gets(str);  // 표준, 빈칸을 포함한 문자열 입력
	fgets(str, 80, stdin); // 최대문자수, stdin-파일 포맷
	puts("입력된 문자열 :");  //배열에 저장된 문자열 출력
	puts(str);  // 임배디드시 사용

	return 0;

}
