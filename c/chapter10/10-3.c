#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//포인터를 이용한 배열의 값 출력
int main() {
	int ary[3] = { 10,20,30 };

	int* pa = ary;
	int i;

	printf("배열의 값 :");

	for (i = 0; i < 3; i++) {

		//printf("%d\n", *pa++);
		printf("%d\n", *pa); //pa가 가리키는 배열 요소 출력
		pa++; // 다음 배열 요소를 가리키도록 pa 값 증가
		//*pa++ 
		printf("%d\n", *pa++);
	}




	return 0;
}
