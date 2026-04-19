#include<stdio.h>

//열거형을 사용한 프로그램

enum season { SPRING, SUMMER, FALL, WINTER };
////SPRING → 0, SUMMER → 1,FALL → 2 ,WINTER → 3

int main() {
    enum season ss;
    char* pc = NULL;

    ss = SPRING;
    switch (ss)
    {
    case SPRING:
        pc = "inline"; break;

    case SUMMER:
        pc = "swimming"; break;

    case FALL:

        pc = "trip"; break;
    case WINTER:

        pc = "skiing"; break;
    }
    printf("나의 레저 활동 =>%s\n", pc);

    return 0;

}
