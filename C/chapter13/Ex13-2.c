#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//배열을 매개변수로 (인자값으로 전달 받았다)
//배열을 return 받아서 사용해 보았다

char* function1(char a) {

	return &a; //return도 포인터로 받을수 있다
}
int* function2(int* pa) {
	return pa;
}

int main() 
{
	char a = 'Y';
	printf("%p\n",function1(a));

	int arr[3] = { 1,2,3 };
	int arr2[3] = { 0, };
	int* pb;

	pb=function2(arr);

	for (int i = 0; i < 3; i++)
	{
		printf("%d\n", arr[i]);//pa[i]
	}




	return 0;
}
