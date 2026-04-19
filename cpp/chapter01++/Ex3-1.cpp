#include<iostream>

int main()
{

	int score;
	std::cout << "점수를 입력하세요";
	std::cin >> score;
	if ((score > 100) || (score < 0)) {
		std::cout << "잘못된 점수 입니다";
		return 0;
	}
	if (score >= 90) {
		std::cout<<"A입니다";
	}
	else if (score >= 80) {
		std::cout << "B입니다";
	}
	else if (score >= 70) {
		std::cout << "C입니다";
	}
	else if (score >= 60) {
		std::cout << "D입니다";
	}
	else { std::cout << "F입니다"; }
}