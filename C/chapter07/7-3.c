#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//반환값이 없는 함수

void print_char(char ch, int count);

int main() {

	print_char('@', 5);

	return 0;
}

void print_char(char ch, int count) {
	int i;

	for (i = 0; i < count; i++) {
		printf("%c", ch);

	}
	return;
}