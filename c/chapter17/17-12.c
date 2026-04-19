#include<stdio.h>

//typedf를 사용한 자료형 재정의

struct student
{
	int num;
	double grade;
};

typedef struct student Student;
void print_data(Student* ps);

int main() {
	Student s1 = { 315,4.2 };

	print_data(&s1);

	return 0;
}

void print_data(Student* ps) {

	printf("학번 : %d\n", ps->num);
	printf("학점 : %.1lf\n", ps->grade);

}