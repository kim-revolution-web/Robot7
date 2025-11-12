#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include<string.h>

//도서명(title), 저자(author), 페이지수(page), 가격(price)를 멤버로 가지는 book 구조체를 선언하세요.
//값을 넣어서 printf()로 출력해 주세요.
//
//도서명 : C 프로그래밍
//
//저자 : 데니스
//
//페이지수 : 180
//
//가격 : 18000



//struct book {
//	const char* title;
//	const char* author;
//	int page;
//	int price;
//};
//
//struct book c;
//c.title = "C 프로그래밍";  // OK
//c.author = "데니스";        // OK
//c.page = 180;


struct book{
	char title[80];
	char author[80];
    int page;
    int price;
};

int main() {

	struct book c = {"C 프로그래밍","데니스",180,18000 };

	/*strcpy(c.title, "C 프로그래밍");*/
	

	


	printf("%s\n", c.title);
	printf("%s\n", c.author);
	printf("%d\n", c.page);
	printf("%d\n", c.price);
	return 0;
}
