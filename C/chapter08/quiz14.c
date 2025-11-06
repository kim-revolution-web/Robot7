#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main() {
	//n 갯수 x 비교 min 값저장
	int arr[10000] = {0};  // c배열에서 모든요소를 0으로 초기화
	int i,n,x= 0;
	
	int min[10000] = { 0 };

	printf("정수 n개입력하세요, 비교 정수 입력하세요");
	scanf("%d %d",&n,&x);
	printf("정수를 입력하세요");
	
	for (i = 0; i < n; i++) {
		scanf("%d", &arr[i]);
		/*printf("arr 값 %d\t", arr[i]);*/
		if (x > arr[i]) {
			min[i] = arr[i];

			printf(" min 값 %d", min[i]);
		}
		
	}




	return 0;
}