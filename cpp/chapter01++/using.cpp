#include<iostream>
#include<ios>
#include<iomanip> //C++ 소수점 구하려면
#include<string>

using std::cin; using std::setprecision;
using std::cout; using std::string;
using std::endl; using std::streamsize;


// P 76.성적 계산 프로그램 C++

int main() {

	//using namespace std::
	//학생의 이름을 묻고 입력받음
	cout << "Please enter your first name:";
	string name;
	cin >> name;
	cout << "Hello," << name << "!" << endl;

	//중간 시험과 기말 시험의 점수를 묻고 입력받음
	cout << "Please enter your midterm and fina exam grades:";
	double midterm, final;
	cin >> midterm >> final;

	//과제 점수를 물음
	cout << "Enter all your homework grades,"
		"follwed by end-of fille:";

	//지금까지 입력된 과제 점수의 개수 와 합
	int count = 0;
	double sum = 0;

	//입력을 위한 변수
	double x; //숙제 성적 

	// 불변성 : 지금까지 count개 점수를 입력 받았으면 입력받은 점수의 합은 sum
	while (cin >> x) { //EOF 입력할 때 거짓!!
		++count;
		sum += x;

	}
	//결과 출력
	streamsize prec = cout.precision(); //초기화
	cout << "Your final grade is" << setprecision(3) //소수점 3자리
		<< 0.2 * midterm + 0.4 * final + 0.4 * sum / count
		<< setprecision(prec) << endl;

	return 0;

}