#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>


int main(int argc, char* argv[]) {

    FILE* fp;
    int ch;


    //명령어 인자가 1개만 실행되지 않게 막아야 한다
    if (argc < 2) {
        printf("다음과 같이 사용하세요 사용법 : %s <파일명 또는 경로>\n", argv[0]);
        exit(2); //프로그램 자체를 종료시켜 버렸다.
    }
    fp = fopen(argv[1], "r"); //textviewer.exe/hom/robot/a.txt 사용법


    if (fp == NULL) {
        printf("파일이 열리지 않았습니다.\n");
        return 1;

    }
    while (1)
    {
        ch = fgetc(fp);
        if (ch == EOF)break;

        putchar(ch);
    }
    fclose(fp);



    return 0;
}