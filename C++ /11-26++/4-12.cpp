#include <iostream>

using namespace std;

class Circle{
    private:
    int radius;
    public:
    Circle(){
        this->radius=1;
    }
    Circle(int radius){
        this->radius=radius;
    }
    //멤버메소드 
    void setRadius(int radius){
        this->radius=radius;
    }
    int getRadius(){
    return this->radius;
    }
};


int main()
{
    Circle c1;
    Circle c2(2);
    Circle c3(3);

    Circle* cp;
    cp = &c1;

    c1.setRadius(4);
    c2.setRadius(5);
    c3.setRadius(6);
    cout<<c1.getRadius()<<endl;
    cout<<c2.getRadius()<<endl;
    cout<<c3.getRadius()<<endl;
    
    return 0;
}