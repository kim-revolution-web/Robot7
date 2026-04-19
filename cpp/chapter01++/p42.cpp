#include<iostream>
#include<string>

//이름을 입력박아 테두리 꾸미기 
int main() {

	std::cout << "첫번째 이름을 입력해주세요";
	std::string name;
	std::cin >> name;

	//출력하려는 메세지를 구성
	 std::string const greeting = "Hello," + name + "!";

	// 인사말의 두 번째 행과 네 번째 행
	const std::string spaces(greeting.size(), ' '); // const로	변수  고정 ' '문자를 ," "문자열
	const std::string second =  '*'  + spaces + "*"; //greeting. 객체 이다 concat 문자열을 붙여준다 

	// 인사말 첫번째 행과 다섯 번째 행
	const std::string first(second.size(), '*');

	//모두 출력
	std::cout << std::endl;
	std::cout << first << std::endl;
	std::cout << second << std::endl;
	std::cout << "*" << greeting << "*" << std::endl;
	std::cout << second << std::endl;
	std::cout << first << std::endl;

	return 0;

}
