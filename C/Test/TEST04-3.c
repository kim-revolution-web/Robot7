#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
//안됨
//포인터 함수
int swap(int a, int b) {

	int temp = 0;
	temp = a;
	a = b;
	b = temp;
}


int main() {

	int a, b;
	int (*fp)(int, int);
	scanf("%d %d", &a, &b);

	printf("%d %d\n", a, b);
	fp = swap;
	
	int res = fp(a, b);


	printf("%d %d\n",res );

	return 0;
};