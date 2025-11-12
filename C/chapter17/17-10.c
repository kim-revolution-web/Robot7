#include<stdio.h>

//공용체를 사용한 학번과 학점 데이터 처리

union  student

{
    int num;
    double grade;    /* data */
};
int main() {
    union  student s1 = { 315 };

    printf("학번 : %d\n", s1.num);
    s1.grade = 4.4;
    printf("학점 : %.1lf\n", s1.grade);
    printf("학번 : %d\n", s1.num);

    return 0;
}