#define _CRT_SECURE_NO_WARNINGS

#include<stdio.h>
//recursive ¹æ½Ä

//5!= 5 4 3 2 1
//      5* 4!= 4 3 2 1
//			4*3!=3 2 1 

int Factorial(int N) {
	
	if (N > 0)
	{
		return	N * Factorial(N - 1);
	}
	else
		return 1;

}


int main() {
	int result =Factorial(5);
	printf("result=%d\n", result);

	return 0;
}