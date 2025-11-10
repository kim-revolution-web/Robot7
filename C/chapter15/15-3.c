#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void print_str(char** pps, int cnt);

int main() {

	//char ptrAry[4][10]; //문자열 배열 상수
	//char* ptr_ary1[4 = { "ealge","tiger","lion","squirrel" };
	char* ptr_ary[4] = { "ealge","tiger","lion","squirrel" };
	char** ptr_ary3 = (char*[]){ "ealge","tiger","lion","squirrel" };
	int count;

	count = sizeof(ptr_ary) / sizeof(ptr_ary[0]);
	print_str(ptr_ary, count);
	

	return 0;
}

void print_str(char** pps, int cnt)
{
	int i;

	for (i = 0; i < cnt; i++)
	{
		printf("%s\n", pps[i]);
	}
}

