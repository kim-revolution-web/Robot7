
#include <iostream>
#include <string>

int main()
{
    std::cout << "Please enter your first name"; // print 출력문
    std::string name; //string 변수 선언 
    std::cin >> name; //scanf 입력문

    //인사말 작성
    std::cout << "Hello," << name << "!" << std::endl; //줄바꿈 + 출력 버퍼 비우기

    return 0;

}
