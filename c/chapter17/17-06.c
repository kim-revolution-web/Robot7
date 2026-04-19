#include<stdio.h>

//구조체 포인터의 사용

struct score
{
    int kor;
    int eng;
    int math;
};

int main() {

    struct score yuni = { 90, 80, 70 };
    struct score* ps = &yuni;
    {
        printf("국어 : %d\n", (*ps).kor);
        printf("영어 : %d\n", ps->kor);
        printf("수학 : %d\n", ps->math);
    };

    return 0;
}