/*
파일을 먼저 읽고 그 다음 파일을 만들어서 써 봅시다
read.txt " I CAN DO IT!!"
write.txt " I CAN DO IT"
*/

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>


int main()
{

    // 1.파일 읽기
    FILE* fin, * fout;
    int ch;

    fin = fopen("read.txt","r");
    fout = fopen("write.txt","w");

    if (fin == NULL) {
        printf("out.txt가 열리지 않았습니다.");
        exit;
    }

    while ((ch = fgetc(fin)) != EOF)
    {

        fputc(ch, fout);
    }
    fclose(fin);
    fclose(fout);

    return 0;
}