#include <stdio.h>
typedef enum 
{
    id,
    pd,
    number
} F;
int main(){ 
F f=id;
char nid=id;
 printf("%d\n",id);
switch(f)
{
    case id:
        printf("id\n");
        break;
    
    case pd:
        printf("pd");
        break;
    
case number:
        printf("number");
        break;
    
}
return 0;
}