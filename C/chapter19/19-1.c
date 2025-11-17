#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>
#include "student.h" //사용자 정의 헤더
//소스 파일
int main() {

	Student a = {315,"홍길동"};

	printf("학번: %d,이름: %s\n",a.num, a.name);


	return 0;
}