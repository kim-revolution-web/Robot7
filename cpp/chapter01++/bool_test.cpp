#include<iostream>

int main() {

	bool b1 = true; // 선언과 동시 초기화
	bool b2 = false;

	std::cout << "b1:" << b1 << std::endl;
	std::cout << "b2:" << b2 << std::endl;


	int a = 100;
	double b = 3.14;

	b = a;// 묵시적인 형변환
	a = (int)b; // 명시적인 형 변환

}

