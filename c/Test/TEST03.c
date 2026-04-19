#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {

	int N = 0;
	printf("정수 하나를 입력하세요");
	scanf("%d", &N);

	if ((90 <= N) && (N <= 100)) {
		printf("A 학점입니다");
	}
	else if (80 <= N){
		printf("B 학점입니다");
	}
	else if (70 <= N) {
		printf("C 학점입니다");
	}
	else if (60 <= N) {
		printf("D 학점입니다");
	}
	else {
		printf("F 학점입니다");
	}
	

	return 0;
};