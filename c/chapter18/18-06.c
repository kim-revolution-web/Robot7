#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//파일의 형태와 개방 모드가 다른 경우
// hexdump -c c.txt
int main() {

    FILE* fp;
    int ary[10] = { 13,10,13,13,10,26,13,10,13,10 };
    int i, res;

    fp = fopen("c.txt", "wb"); //바이너리 파일로 개방
    for (i = 0; i < 10; i++)
    {
        fputc(ary[i], fp); // 배열 요소의 각 값에 해당하는 아스키 문자 출력
    }
    fclose(fp); //파일 닫음

    fp = fopen("a.txt", "rt");
    while (1) {
        res = fgetc(fp);
        if (res == EOF) break;
        printf("%4d", res);
    }
    fclose(fp);

    return 0;
}