#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//최고 학점의 학생 데이터 출력

struct student
{
	
	int id;
	char name[20];
	double grade;
};

int main() {

	struct student 
		s1 = { 315, "홍길동",26.3 },
		s2 = { 316, "이순신",37.4 },
		s3 = { 317, "세종대왕",44.5 };

	struct student max;

	max = s1;
	if (s2.grade > max.grade)max = s2;
	if (s3.grade > max.grade)max = s3;

	printf("학번 : %d\n", max.id);
	printf("이름 : %s\n", max.name);
	printf("학점 : %.1lf\n", max.grade);
	
	return 0;
}
