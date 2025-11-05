#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//구구단
int main() {

	for (int j = 2; j < 10; j++) {
		for (int i = 1; i < 10; i++) {
			printf("%d * %d =%d\n", j, i, j * i);
		}
		printf("\n\n");
	}


	return 0;
}
