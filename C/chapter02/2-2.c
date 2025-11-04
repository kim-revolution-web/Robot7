#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//문자열을 화면에 출력하는 프로그램
int main()
{
	printf("Be happy\n"); // "Be happy"를 출력하고 줄을 바꿈(\n)
	printf("12345678901234567890\n"); // 화면에 열 번호 출력하고 줄을 바꿈(\n)
	printf("My\tfriend\n");//"My"를 출력하고 탭 위치로 이동(\t) 후에 "friend"를 출력하고 줄을 바꿈(\n)
	printf("Goot\bd\tchance\n"); // "Goot"를 출력하고 칸 왼쪽으로 이동(\b)해
	//t를 d로 바꾸고 탭 위치로 이동(\t) 후에 "change" 를 출력하고 줄을 바꿈(\n)
	printf("Cow\rW\a\n");
	//맨 앞으로 이동(\r)해 C를 W로 바꾸고 벨소리(\a)를 내고 줄을 바꿈(\n)

	printf("power\r\a\n");
	//이동만 하면 변화가 없음
	printf("toucc\by mc\by bodc\by");
	// /b를 쓴 왼쪽으로 한칸이동

	return 0;


}
