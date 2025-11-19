#include<iostream>

int main() {

    using namespace std;

    cout << "이름을 입력하세요 :";

    string name; // 문자열 대신 string 으로 씀 
    cin >> name;

    cout << "이름은 " << name << "입니다." << endl;
    return 0;

}