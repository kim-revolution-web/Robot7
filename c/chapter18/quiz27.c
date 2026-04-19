#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {

    FILE* fp;
    char str[] = "블루베리";
    fp = fopen("fruits.txt", "w");

    if (fp == NULL)
    {
        printf("파일을 만들지 못했습니다.\n");
        return 1;
    }
    for (int i = 0; str[i] != '\0'; i++) {
        fputc(str[i], fp);
    }
    fputc('\n', fp);
    fclose(fp);

    return 0;
}