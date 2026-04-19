#include <stdio.h>

// 표준 입출력 스트림을 사용한 문자열
int main()
{

    int ch;
    while (1)
    {

        // ch= getchar();
        ch = fgetc(stdin);
        if (ch == EOF) //wsl ubuntu ^z --> ^c 종료했음 
            break;

        putchar(ch);
    }
    return 0;
}