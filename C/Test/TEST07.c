#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {

	int n = 0;
	
	for (int i = 2; i < 100; i++) {
		for (int j = 2; j < 100; j++) {
			if (i % j != 0) {
				++n;
				
			}
			
		}
		if (n == 1) {
			printf("%d\n", i);
		}

	}


	return 0;
};
