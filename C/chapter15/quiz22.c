#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>


void print_array(char* arr);

int main()

{

	char arr[5] = { 'A', 'B', 'C', 'D', 'E' };



	print_array(arr);
	return 0;
}

void print_array(char* arr)

{
	for (int i = 0; i < 5; i++) {
		printf("%c", arr[i]);
	}
	//구현하세요~!!!

}

//------------------------------ -

//A B C D

