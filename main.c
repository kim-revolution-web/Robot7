#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {

	int score[3] = { 0 };// 0,1,2 지만 score[3]는 NULL이 들어있나? ,0초기화는 안되지만 {0} 초기화 가능?
	int total=0;
	double avg = 0.0;

	printf(" 3 과목의 점수를 입력하세요 :\n");
	// 3번 받을것을 반복문으로 받아준다
	for (int a = 0; a < 3; a++) {
		scanf("%d", &score[a]);
		printf("%d 번쨰 과목, %d :과목점수\n",a,score[a]);
		printf(" 뭐가 들어 있니? : %d\n ",score[3]);
		total += score[a];
		avg = total/3.0;// 반복문 안에있어서 total 값이 다 더해진 상태후 나눠져서 잘 나옴


	}
	/*avg = total / 3.0;*/
	printf("total 값:%d:\n",total);
	printf("avg 값: %.2lf\n", avg);

	return 0;
}