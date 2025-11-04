#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//전위 표기와 후위 표기를 사용한 증감 연산

int main() {

	int a = 5, b = 5;
	int pre, post;

	pre = (++a)*3; //전위형이라 증가하고 계산
	post = (b++)*3;// 후위형이라 계산 후 증가 

	//pre = (++a);, post = (b++); 이렇게 증가감 연산자가 한줄에 같이 쓰이면 안됨

	printf("%d,%d\n",a,b);
	printf("%d,%d\n,",pre,post);

	return 0;

}

