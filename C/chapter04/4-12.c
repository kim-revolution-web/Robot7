#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {

	int a = 10, b = 20, res;

	res = (a > b) ? a : b;

	printf("큰값 %d:\n", res);
	
	
	/*if (a > b) {
		
		res = a;
	}
	else {
		res = b;
	}

	printf("값 : %d\n", res);*/


	return 0;
}
