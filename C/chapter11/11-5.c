#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//입력 문자의 아스키 코드 값을 출력하는 프로그램
int main() {

	int res;
	char ch;
	
	while (1)
	{
		res = scanf("%c",&ch);
		/*printf("%d", res);*/

		if (res == -1)break;

		printf("%d",ch);

	}


	return 0;
}
