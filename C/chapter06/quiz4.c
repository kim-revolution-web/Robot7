#define _CRT_SECURE_NO_WANRINGS
#include <stdio.h>

int main() {


	int a = 3;
	int i=1;
	/*int sum = 0;*/

	while (i < 10) {
		
		/*sum=a*i ;*/
	printf("%d*%d = %d\n",a,i ,a*i);
	i++;

	}

	/*char b = 'A';

	for (i = 0; i <= 25; i++) {
		sum = b + i;
		printf("%c", sum);

	}*/
	
	
	for (i = 'A'; i <= 'Z'; i++) {
		printf("%c", i);
	}
	printf("\n");

	for (i = 'a'; i <= 'z'; i++) {
		printf("%c", i);
	}

	return 0;
}