#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//입력 문자의 아스키 코드 값을 출력하는 프로그램
int main() {

	int res;
	char ch;

	while (1)
	{
		res = scanf("%c", &ch);
		//printf("%d", res);
		//\n 개행까지 버퍼에 저장 \n==10;
		
		if (res == -1)break;
		//-1==EOF
		printf("%d", ch);

	}


	return 0;
}
