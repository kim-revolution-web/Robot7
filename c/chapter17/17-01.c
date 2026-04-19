#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//구조체를 선언하고 멤버를 사용하는 방법
struct student
{
	int num; //학번
	double grade; //학점
};
int main() {

	struct student gildong; //구조체 초기화

	gildong.num = 2;
	gildong.grade = 3.4;

	printf("길등이의 학번 :%d\n", gildong.num);
	printf("길등이의 성적 :%.1lf\n", gildong.grade);


	return 0;
}
