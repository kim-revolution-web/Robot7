#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// 파일의 내용을 화면에 출력하기
int main() {

    FILE* fp;
    int ch;

    /*char* path = "/home/robot/work/basic/chapter18/a.txt";
    fp = fopen(path, "r");*/

    fp = fopen("a.txt","r");
    if (fp == NULL) {
        printf("파일이 열리지 않았습니다.\n");
        return 1;

    }
    while (1)
    {
        ch = fgetc(fp); //한글자를 가져오는 함수
        if (ch == EOF)break; //(-1)파일의 끝 

        putchar(ch); //printf("%c",ch);
    }
    fclose(fp); //자원 (Resource) 반환



    return 0;
}