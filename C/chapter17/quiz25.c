#include <stdio.h>

//완전수
int main()
{
    int n;
    int sum = 0;
    printf("1000이하의 수를 구하시오\n");
    scanf("%d", &n);
    for (int i = 1; i < n; i++)
    {
        if (n % i == 0)
            sum += i;
    }

    if (n == sum)
    {
        printf("완전수 %d\n", n);
    }
    else{
        printf("완전수가 아니다");
    }

    return 0;
}
