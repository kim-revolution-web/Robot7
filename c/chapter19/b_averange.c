//분할 컴파일에서 extern과 static의 용도
#define _CRT_SECURE_NO_WARNINGS
//average 함수 정의

extern int count;
extern int total;

double average() {
	return total / (double)count;
}