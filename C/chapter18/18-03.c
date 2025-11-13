#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// 문자열을 한 문자씩 파일로 출력하기
int main() {

    FILE* fp;
    char str[] = "banana";
    int i=0;

    fp = fopen("b.txt", "w");
    if (fp == NULL) //fopen 의 정상동작 유뮤
    {
        printf("파일을 만들지 못했습니다.\n");
        return 1;
    }
    while (str[i] != '\0') {
        fputc(str[i], fp);
        //fputs(str,fp);
        //fprintf(fp,"%c",str[i]);

        i++;

    }
    fputc('\n', fp);
    printf("만들었다");
    fclose(fp);

    return 0;
}