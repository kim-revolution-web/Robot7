#include<iostream>

int g = 20; //전역 변수

int add(int x, int y) {
	return x + y;
}

int main()
{
	/*using namespace std:*/
	
	int a, b, sum;
	std::cout << "두정수를 입력하세요";
	std::cin >> a >> b;

	sum = add(a, b);

	std::cout << a <<":"<< b << std::endl;
	std::cout << "두 수의 합은 " << sum << std::endl;
	return 0;

}