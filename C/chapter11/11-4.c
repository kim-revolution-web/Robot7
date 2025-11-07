#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//버퍼를 사용하는 문자 입력

int main() {

	char ch;
	int i;
	for (i = 0; i < 3; i++) {

		scanf("%c", &ch);
		printf("%c", ch);
	}


	return 0;
}
