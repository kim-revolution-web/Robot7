#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//Q11) 배열의 요소 중 가장 큰값을 출력해 주세요.단, 함수로.

void print_max(int* pa) // (int p[])
{
	int i = 0;
	int max = 0;
	for (i = 0; i < 7; i++) {
		if (max < pa[i]) 
		{
			max = pa[i];
		}
		
	}
	printf(" max :%d\n",max);
	
}

int main() {

	int array[7] = {4,5,8,1,2,3,7};
	print_max(array);

	return 0;
}