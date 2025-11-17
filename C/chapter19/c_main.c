#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "c_line.h" //Line 구조체 선언
#include "c_point.h" //Point 구조체 선언

int main()
{
	Line a = { {1,2},{5,6} };// Line 구조체 변수 초기화
	Point b; // 가운데 점의 좌표 저장

	b.x = (a.first.x + a.second.x) / 2; //가운데 정의 x좌표 계산
	b.y = (a.first.y + a.second.y) / 2; //가운데 정의 y좌표 계산
	printf("선의 가운데 점의 좌료: (%d,%d)\n", b.x, b.y);

	return 0;
}

