#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//getchar 함수와 putchar 함수 사용
//한글자 받기
int main() {

	int ch; //입력 문자를 저장할 변수

	//getchar :int(정수) 타입이라 int를 쓴다
	ch = getchar(); // 함수가 반환하는 문자를 바로 저장
	printf("입력한 문자 : ");
	putchar(ch); //입력한 문자 출력
	putchar('\n'); // 개행 문자 출력

	

	return 0;
}