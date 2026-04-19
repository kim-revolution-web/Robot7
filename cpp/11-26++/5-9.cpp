#include <iostream>

using namespace std;

class Circle
{
    int radius;

public:
    Circle(int radius)
    {
        this->radius = radius;
    }
    Circle(const Circle &other)
    {
        cout<<"복사 생성자 실행!!";
        this->radius=other.radius;

    }
    
    int getArea() { 
        return 3.14*radius*radius; }
};
int main()
{
    Circle src(30); // 매개변수가 1개인 생성자로 생성
    Circle dst(src); //매개변수가 객체인 생성자로 값을 복사후 생성!.

    cout<< "사본의 면적:"<<dst.getArea()<<endl;
    return 0;
}