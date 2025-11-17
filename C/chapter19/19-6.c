#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#define VER 7
#define BIT16

//#if,ifdef,$else,#endif를 사용한 조건부 컴파일

int main() {

    int max;

#if VER>=6
    printf("버전 %d입니다.\n", VER);
#endif

#ifdef BIT16
    max = 32767;
#else
    max = 2147483647;
#endif

    printf("int형 변수의 최댔값 : %d\n", max);

    return 0;
}