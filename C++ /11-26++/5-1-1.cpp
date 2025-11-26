#include <iostream>


using namespace std;

class Circle{
private:int radius;

public:
Circle(int radius){
    this->radius=radius;
    cout<<"생성자 실행 radius="<<this->radius<<endl;
}
~Circle(){
    cout<<"소멸자 실행 radius="<<this->radius<<endl;
}
int getRadius(){
    return this->radius;
}
void setRadius(int radius){
    this->radius=radius;
}
};

void increase(Circle c){
    int r=c.getRadius();
    c.setRadius(r+1);
}
int main()
{
    Circle waffle(30);
    increase(waffle);
    cout<<"현재 waffle의 반지름은??:"<<waffle.getRadius()<<endl;
    return 0;
}