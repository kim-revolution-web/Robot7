#include <iostream>

using namespace std;

class Circle{
    int radius;
    public:
    Circle(){radius =1;}
    Circle(int radius){this->radius =radius;}
    void setRadius(int radius){this->radius =radius;}
    double getArea(){return 3.14*radius*radius;}
};
int main()
{
    Circle circle;
    Circle &ref =circle; //ref 레퍼런스, *ref-> 객체
    ref.setRadius(10);
    cout<<ref.getArea()<<" "<<circle.getArea();


    return 0;
}