#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//auto 지역 변수와 static 지역 변수의 비교
void auto_func(); // auto_func 함수 선언
void static_func１(); // static_func 한수 선언
void static_func２();

int main() {
	int i;

	printf("일반 지역 변수(auto)를 사용한 함수 .. \n");
	for (i = 0; i < 3; i++)
	{
		auto_func();
	}
	printf("정적 지역 1 변수 (static)를 사용한 함수...\n");
	for (i = 0; i < 3; i++) {

		static_func１();

	}
	printf("정적 지역 2 변수 (static)를 사용한 함수...\n");
	for (i = 0; i < 3; i++) {

		static_func２();

	}
	return 0;
}

void auto_func()
{
	auto int a=0;

	a++;
	printf("%d\n", a);

}

void static_func１()//정적 지역 변수
{
	static int a;
	a++;
	printf("%d\n", a);
}

void static_func２()//정적 지역 변수
{
	static int a;
	a++;
	printf("%d\n", a);
}