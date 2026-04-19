#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//중첩 if문에서 중괄호가 반드시 필요한 경우
int main() {

	int a = 10,b = 20;

	if (a > 0) {

		if (b > 0) {
			printf("ok");
		}
	}
	else {
		printf("NO");
		
	}


	return 0;
}
