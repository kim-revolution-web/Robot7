
#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// 재귀 호출 함수
void fruit() {

	printf("apple\n");
	fruit();

}

int main() {

	fruit();

	return 0;
}


