#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//문자열을 출력하는 puts와 fputs 함수
int main() {

	char str[80] = "apple juice";
	char* ps = "banana";

	puts(str); //apple juice 출력하고 줄 바꿈 puts \n포함 
	fputs(ps, stdout); //banana만 출력
	puts("milk");// banana에 이어 milk 출력

	return 0;
}
