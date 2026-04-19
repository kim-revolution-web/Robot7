#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//if ~else if ~else 문 사용 
int main() {

	int a = 7, b = 0;
	if (a > 8) {  //조건식1
		b = 1;    //실행문1
	}
	else if (a == 7) { // 조건식2
		b = 2;       // 실행문2
	}
	else {
		b = 3; // 실행문3
	}

	printf("b: %d\n", b);

	return 0;
}
