
#include <stdio.h>
#include <stdlib.h>
#include<string.h>


int main()
{
    char str[50];
    printf("문자열을 입력하세요 :");

    fgets(str, 80, stdin);
    printf("%s\n", str);

    return 0;
}
