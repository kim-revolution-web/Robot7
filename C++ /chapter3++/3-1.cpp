#include <iostream>

class Circle
{
public:
//1.멤버 변수
    int radius;
    //2. 생성자
    //없으면 컴파일러가 컴파일 시 자동으로 생성
    //3. 멤버함수

    double getArea()
    {
        return 3.14 * radius * radius;
    };
};

int main()
{
    using namespace std;
    Circle donut; // stack 객체가 만들어집니다.

    donut.radius = 1;
    donut.getArea();
    cout<<"donut"<<donut.getArea()<<endl;

    Circle pizza;
    pizza.radius = 30;
    cout<<"donut"<<pizza.getArea()<<endl;



    


    return 0;
}