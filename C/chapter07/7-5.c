
#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

void fruit() {

	printf("apple\n");
	fruit();

}

int main() {

	fruit();

	return 0;
}

