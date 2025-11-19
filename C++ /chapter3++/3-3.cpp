#include<iostream>

//객체가 만들어 질 때 생성자와 맞는 인자를 출력된다 
using namespace std;
class Circle{

    public:
    //1.멤버 변수 생성자 == 매소드
    int radius;
    string color;

    //2. 생성자

    Circle() // default  생성자
    {
        this->radius=1;
        cout << "circle 의 반지름: " << radius<<endl;
    }

    Circle(int r) // 매개변수 전달 생성자 
    {
        this->radius=r;
        cout << " 반지름: " << radius<<endl;
    }

    Circle(int r,string c) // 매개변수 전달 생성자 
    {
        this->radius=r;
        this->color=c;
        cout << " 반지름: " << radius<<"색상:"<<color<< endl;
    }



    //3. 멤버 메소드

};


int main(){

    
    Circle donut;
     Circle pizza(30);
     Circle tire(10,"RED");
     //객체는 생성자와 관련이 있다

    

    return 0;
}