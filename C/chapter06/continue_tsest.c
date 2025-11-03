#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {


	for (int i = 0; i < 10; i++) {

		if (i % 7 == 0)
			continue;
		printf("%d\n", i);
	}
	
	for (;;) {
		printf("Hello\n");

	}

	while (1) {
		printf("Hello\n");
	}


	return 0;
}