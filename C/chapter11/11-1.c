#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//대문자를 소문자로 변경
int main() {

	char small, cap = 'G';

	if (('Z' >=cap ) && (cap >= 'A')) {

		small = cap + ('a' - 'A');


	}
	printf("대문자 : %c %c", cap, '\n');
	printf("소문자 : %c", small);



	return 0;
}