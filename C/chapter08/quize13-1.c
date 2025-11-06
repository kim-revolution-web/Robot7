#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//배열과 반복문을 사용한 성적 처리 프로그램
int main() {

	int score[10];
	int i;
	int multiple_of_2[5] ;
	int max =0;
	int index = 0;
	// 짝수번째 만 출력
	for (i = 0; i < 10; i++) {

		scanf("%d", &score[i]);

	}
	
	for (i = 0; i < 10; i++) {
		
		if (score[i] % 2 == 0) {
			
			printf("2의 배수 %5d\n", score[i]);
		}
		
		//배열의 최대값과 index를 구하라.
		if (max > score[i]==0) {
			max = score[i];
			index = i;
		}
		
	}
	printf("index %5d\n", index);
		printf("가장 큰수 %5d\n", max);
	if (3 < 2 == 1) printf("확인\n"); 
	
	return 0;
}