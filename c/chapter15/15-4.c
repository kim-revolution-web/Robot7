#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//주소로 쓰이는 배열명과 배열의 주소
int main() {

	int ary[5];

	printf(" ary의 값 : %u\t", ary); // 주소로서의 배열명의 값
	printf(" ary의 주소 : %u\t", &ary); // 배열의 주소
	printf(" ary+1 : %u\t", ary+1);
	printf(" &ary+1 : %u\t", &ary+1);



	return 0;
}
