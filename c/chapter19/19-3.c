#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#define SUM(a,b)((a) +(b)) // 두 값을 더하는 매크로 함수
#define MUL(a,b)((a) *(b)) // 두 값을 곱하는 매크로 함수

//매크로 함수를 사용한 프로그램
int main() {

    int a = 10, b = 20;
    int x = 30, y = 40;
    int res;

    printf("a + b =%d\n", SUM(a, b)); // a와 b의 합
    printf("x + y =%d\n", SUM(x, y)); // x와 y의 합
    res = 30 / MUL(2, 5); // 30을 2와 곱으로 나눔
    printf("res : %d\n", res);



    return 0;
};