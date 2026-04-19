#include <iostream>

// 객체가 만들어 질 때 생성자와 맞는 인자를 출력된다
using namespace std;
class Circle
{

public:
    // 1.멤버 변수 생성자 == 매소드
    int radius;
    string color;

    // 2. 생성자

    Circle():radius(1),color("RED") // 초기화 변수
    {
        //this->radius = 1;
        cout << "circle 의 반지름: " << radius << endl;
        cout << "색상 " << radius << endl;
    }

    Circle(int r):radius(r) // 매개변수 전달 생성자
    {
        this->radius = r;
        cout << " 반지름: " << radius << endl;
    }

    // 3. 멤버 메소드
};

int main()
{

    Circle donut;
    Circle pizza(30);

    return 0;
}