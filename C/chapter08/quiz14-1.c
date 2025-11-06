#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>



int main()

{

    int a, x;

    int num;

    scanf("%d %d", &a, &x);

    for (int i = 0; i < a; i++)

    {

        scanf("%d", &num);

        if (x > num)

        {
            printf("%d ", num);

        }

    }



}