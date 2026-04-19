#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>


void print_array(char** arr,int count);
void print_array1(char** arr, int count);

int main()

{

	char *arr[3] = { "Lion", "Tiger", "Rabbit" };
	int count = sizeof(arr) / sizeof(arr[0]);
	int count1 = sizeof(arr[0]) / sizeof(arr[0][0]);
	print_array(arr,count);
	print_array1(arr, count);

	
	return 0;
}

void print_array(char** arr,int count)

{
	
	for (int i = 0; i < count; i++) {
		printf("%s\n", arr[i]);

	}
	
}

void print_array1(char** arr, int count1)

{

	char* pa;
	pa = *arr;
	for (int i = 0; i < count1; i++) {
		printf("%c\n", pa[i]);
		//구현하세요~!!!
	}

}



//------------------------------ -

//A B C D

