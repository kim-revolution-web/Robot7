#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h> //해더가 있어야 작동한다

//
int main() {

	char str1[80] = "cat";
	char str2[80];

	strcpy(str1, "tiger");
	strcpy(str2, str1);
	printf("%s, %s\n", str1, str2);

	return 0;

}
