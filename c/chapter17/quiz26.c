#include <stdio.h>

//약수
int main()
{
    int n=0;
  
    printf("100이하의 수를 구하시오\n");
    for (int i = 2; i < 100; i++)
    {
        for(int j=2; j<i;j++){
            if(j%i!=0){
            n=1;
            break;
            }

        }
        if(n==0)printf("%d",i);
    }
return 0;
}
