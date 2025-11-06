#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
//알파벳 a~z까지 고르고
	//A~Z까지고르고
	//숫자 고르고
	//특수문자 고르고
	//if 할까? 아니면 포인터로 주소 값으로 매개변수에 던질까?


int main() {

	char str[80] = { 0, };
	char a;
	char B;
	char num;
	char text;
	char size;

	/*size = sizeof(arr) / sizeof(arr[0]);*/
	scanf("%s", str);
	int cntBig = 0, cntSmall = 0, cntNumber = 0, cntSpecial = 0;
	
	for (int i = 0; i < strlen(str); i++) {
		if ((str[i] >= 'A') && (str[i] <= 'Z')) cntBig++;
		else if ((str[i] >= 'a') && (str[i] <= 'z')) cntSmall++;
		else if ((str[i] >= '0') && (str[i] <= '9')) cntNumber++;
		else cntSpecial++;
	}
	printf("대문자 : %d\n", cntBig);
	printf("소문자 : %d\n", cntSmall);
	printf("대문자 : %d\n", cntNumber);
	printf("대문자 : %d\n", cntSpecial);

	return 0;
}

//char a (char* p,char size){
//	for(char a='a';a<='z';'a'++)
//}