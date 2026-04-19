#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//버퍼의 내용을 지워야 하는 경우
//공부용 좋지 않은 코드
int main() {

	int num, grade;

	printf("학번 입력 :");
	scanf("%d", &num); //학번 입력
	getchar(); //버퍼에 남아 있는 개행 문자 제거
	printf("학점 입력 :");
	grade = getchar(); // 학점 입력
	printf("학번 : %d,학번 : %c", num, grade);



	return 0;
}
