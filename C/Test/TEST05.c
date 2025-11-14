#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {
	
	for (int i = 9; i >1; i--) {
		for (int j = 1; j < 10; j++) {
			printf("%d * %d = %d\n",i,j,i*j);
		}
		puts("\n");
	}


	return 0;
};