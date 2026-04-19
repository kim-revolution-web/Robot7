
#include <iostream>
#include <string>

int main()
{

    using namespace std;

    string song;//문자열 변수 선언
    song = "Falling in love with you";//문자열 변수 초기화 문자열 대입 초기화
    string elvis("Elvis Presley");//선언과 동시 문자열 초기화

    string singer; //문자열 변수 선언만

    cout << song + "를 부른 가수는?\n";
    cout << "(힌트 : 첫글자는" << elvis[0] << ")?\n";

    getline(cin, singer); // 문자
    if (singer == elvis)
        cout << "맞았습니다.";
    else
        cout << "틀렸습니다." + elvis + "입니다." << endl;//+로 문자열 연결

    return 0;
}