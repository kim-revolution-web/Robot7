#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {
	int rank = 3, m = 0;

	switch (rank) { //rank의 값이 얼마이지 확인
	
	case 1: //rank가 1이면  
		m = 300; //m= 300을 수행하고
		break; //블록을 벗어나 22행으로 이동
	case 2: //rank가 2이면  
		m = 200; //m= 200을 수행하고
		break; //블록을 벗어나 22행으로 이동
	case 3:
		m = 100; //m= 100을 수행하고
		break; //블록을 벗어나 22행으로 이동
	default:
		m = 10; //m= 10을 수행하고
		break; //블록을 벗어나 22행으로 이동

	}

	printf("m : %d\n", m);

	//switch 문을 if문으로 변환
	if (rank == 1) {

		m = 300;
		printf("m: %d\n", m);
	}
	else if (rank == 2) {
		m = 200;
		printf("m: %d\n", m);
	}
	else if (rank == 3) {
		m = 100;
		printf("m: %d\n", m);

	}
	else {
		m = 10;
		printf("m: %d\n", m);
	}


	return 0;
}
