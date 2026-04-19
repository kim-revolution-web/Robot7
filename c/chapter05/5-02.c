#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//if ~else문의 사용

int main() {

	int a = -7;
	if (a >= 0){
		a=1;
	}
	else {
		a = -1;
	}
	printf("a값은 :%d", a);
	return 0;

}

