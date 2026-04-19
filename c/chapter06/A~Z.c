#define _CRT_SECURE_NO_WANRINGS
#include <stdio.h>

//A~Z
int main() {


	int a = 3;
	int i = 1;
	/*int sum = 0;*/

	while (i < 10) {

		/*sum=a*i ;*/
		printf("%d*%d = %d\n", a, i, a * i);
		i++;

	}
	//A~Z 까지 아스키코드 번호로 만들기
	/*char b = 'A';

	for (i = 0; i <= 25; i++) {
		sum = b + i;
		printf("%c", sum);

	}*/

	//A~Z까지 문자로 넣어서 만들기
	for (i = 'A'; i <= 'Z'; i++) {
		printf("%c", i);
	}
	printf("\n");

	for (i = 'a'; i <= 'z'; i++) {
		printf("%c", i);
	}

	return 0;

}
