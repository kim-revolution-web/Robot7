#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h> //문자열을 다룰 수 있는 string.h 헤더 파일 포함

//char 배열에 문자열 복사

int main() {

	char fruit[20] = "strawberry"; //strawberry로 초기화
	//길이 20안으로 들어오는 건 변화 가능

	printf("%s\n", fruit); //strawberry 출력
	strcpy(fruit, "banana"); //fruit 에 banana 복사
	printf("%s\n", fruit); // banana 출력
	strcpy(fruit, "everything"); 
	printf("%s\n", fruit);
	strcpy(fruit, "everything banana strawberry"); 
	//에러남 문자열 크기보다 커서 NULL이랑 공백 포함 29까지 있어야한다
	printf("%s\n", fruit);

	return 0;
}