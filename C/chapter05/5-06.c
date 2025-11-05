#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>


int main() {
	int rank = 3, m = 0;

	switch (rank) {
	case 1:
		m = 300;
		break;
	case 2:
		m = 200;
		break;
	case 3:
			m = 100;
			break;
	default:
			m = 10;
			break;

	}

	printf("m : %d\n", m);

	//switch 문을 if문으로 사용
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