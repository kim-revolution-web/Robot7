#define _CRT_SECURE_NO_WANINGS
#include<stdio.h>

int main() {

	int i = 0;//초기값
	int sum = 0;
	while (i<100) {
		
		i++;
		sum += i;


		
	}
	printf("%d까지 합 :%d\n", i, sum);
	return 0;

}