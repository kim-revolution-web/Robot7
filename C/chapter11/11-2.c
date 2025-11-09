#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//공백이나 제어 문자의 입력
int main() {

	char ch1, ch2;

	//scanf("%c%c", &ch1, &ch2);
	//// 2개의 문자를 연속 입력
	//printf("[%c%c]\n", ch1, ch2);
	//// 띄어쓰하면 문자 하나 출력이 안됨

//----------------------------------
	//입력된 문자 출력
	scanf("%c %c", &ch1, &ch2);
	// 화이트 스페이스
	printf("화이트 스페이스[%c%c]\n", ch1, ch2);

	fflush(stdin); // TC(XXXX); 해결 불가능하다

	return 0;
}
