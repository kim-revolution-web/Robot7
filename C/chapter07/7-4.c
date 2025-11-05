#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//반환 값과 매개 변수가 모두 없는 함수

void print_line();


int main() {

	print_line();
	printf("학번\t이름\t전공\t학점\n");
	print_line();

	return 0;
}

void print_line() {

	for (int i = 0; i < 50; i++) {
		printf("-");
	}
	printf("\n");

}
