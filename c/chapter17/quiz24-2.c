#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
//#include<string.h>

//크래커의 가격과 열량을 저장할 크래커 구조체 선언
//
//-------------------------------------------------- -
//
//바사삭 가격과 열량을 입력하세요 : 1200 500
//
//바사삭 가격 : 1200원
//
//바사삭 열량 : 500kcal

struct cracker {
	
	int price;
	int kcal;
};

int main() {

	/*struct book c = {"C 프로그래밍","데니스",180,18000 };*/

	/*strcpy(c.title, "C 프로그래밍");*/
	struct cracker c;

	scanf("%d %d", &(c.price), &(c.kcal));

	printf("%d\n", c.kcal);
	printf("%d\n", c.price);
	
	return 0;
}
