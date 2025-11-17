#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//이미 정의된 매크로의 기능
void func(); //함수 헤더

int main() {

    printf("컴파일 날짜와 시간 :%s, %s\n\n", __DATE__, __TIME__);
    printf("파일명 : %s\n", __FILE__);
    printf("함수명 : %s\n", __FUNCTION__);
    printf("행번호 : %d\n", __LINE__);

    func();


    return 0;
}
void func() {

    printf("\n\n");

    printf("파일명 : %s\n", __FILE__);
    printf("함수명 : %s\n", __FUNCTION__);
    printf("행번호 : %d\n", __LINE__);


}