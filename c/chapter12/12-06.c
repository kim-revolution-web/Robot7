#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//개행문 문자로 인해 gets 함수가 입력을 못하는 경우
int main() {

	int age;
	char name[20];

	printf("나이 입력 :");
	scanf("%d", &age); //scanf 함수로 나이 입력

	printf("이름 입력 :");
	gets(name); //gets 함수로 이름 입력
	printf("나이 : %d,이름 : %s\n", age, name);


	return 0;
}
