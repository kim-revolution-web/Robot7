#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Circle{

    public:
    int radius;
    Circle(int r){
        radius =r;
    }
    void draw(){
        cout<<"그리다"<<endl;
    }
};


int main()
{//기본타입 동적 할당
    int* p =new int; // bool
    *p=5;
    delete p;

    //배열 동적 할당
    int* p2 = new int[3];
    p2[0]=0;
    p2[1]=1;
    delete[]p2;

    //c++11 스마트 포인터 <class Type>
    unique_ptr<int> p3 = make_unique<int>(5);
    unique_ptr<Circle> p4 = make_unique<Circle>(10);
    p4->draw();

    return 0;
}