#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//명령행 인수를 출력하는 프로그램
int main(int argc,char **argv) {

	int i;

	for (i = 0; i < argc; i++)
	{
		printf("%s\n", argv[i]);
	}

	return 0;
}
