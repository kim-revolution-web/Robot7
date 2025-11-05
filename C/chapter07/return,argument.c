#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

//1. return(x), argument(x)
void myprint() {
	printf("myprint()\n");
}

//2. return(o), argument(x)
char mychar() {
	return 'Z';
}

//3. return(x), argument(o)
char myint(int a) {
	printf("%d\n", a);
}

//4. return(o), argument(o)
int myint2(int b) {
	return b;
}

//5. return(o), argument(o)
int sum(int a,int b, int c) {
	
	int result = a + b + c;
	return result;

}


int main() {

	myprint();
	char c = mychar();
	printf("%c\n", c);
	myint(5550);
	int result = myint2(7777);
	printf("%d\n", result);
	printf("%d\n", sum(100,200,300));
	return 0;

}
