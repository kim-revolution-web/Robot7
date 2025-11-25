#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#define VER 7
#define BIT16

//#if,ifdef,$else,#endif를 사용한 조건부 컴파일

int main() {

    int max;

#if VER>=6 //전처리 if문 
    printf("버전 %d입니다.\n", VER);
#endif

#ifdef BIT16  //매크로가 정의 되어 있으면 실행 #ifndef 이 매크로가 정의 되어 있지 않으면 실행
    max = 32767;
#else
    max = 2147483647;
#endif

    printf("int형 변수의 최댔값 : %d\n", max);

    return 0;
}
