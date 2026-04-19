#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//배열과 반복문을 사용한 성적 처리 프로그램
int main() {

	int score[5];
	int i;
	int total = 0;

	for (i = 0; i < 5; i++) {

		scanf("%d", &score[i]);
		
	}
	// total = score[0] + score[1] + score[2] + score[3] + score[4];
	for (i = 0; i < 5; i++) {
		//total = total + score[i];
		total += score[i];
		printf("%5d", score[i]);
		
	}

	double avg = (double)total / 5.0;

	for (i = 0; i < 5; i++) {

		
	}
	printf("\n");
	printf("%.1lf",avg);
	return 0;
}
