#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Car{
    private:
    string brand;
    int speed;
    string color;

    Car(const string &b, int s, const string &c) //생성자의 선언/헤더
    :brand(b), speed(s),color(c)//멤버 초기화 리스트
    {}
    public:
    class Builder{
        private:
        string brand="기아";
        int speed=0;
        string color="파랑";
        public:
        Builder &setBrand(const string &b){
            this->brand=b;
            return *this;
        }
        Builder &setSpeed(int s){
            this->speed=s;
            return *this;
        }
        Builder &setColor(const string &c){
            this->color=c;
            return *this;
        }
        Car build(){
            return Car(brand,speed,color);
        }

    };
string getBrand(){return brand;}
int getSpeed(){return speed;}
string getColor(){return color;}

};

int main()
{
    Car car = Car::Builder()//임시 Builder 객체 생성
    .setBrand("삼성")//체이닝으로 빌더 세팅
    .setSpeed(100)
    .setColor("빨강")
    .build();//build()가 Car 객체를 값으로 반환
    cout<<"브랜드:"<<car.getBrand()<<endl;
    cout<<"속도:"<<car.getSpeed()<<endl;
    cout<<"색상:"<<car.getColor()<<endl;
//그래서 눈에 보이는 “깊은 복사 / 얕은 복사” 개념보다는
//“함수 반환값으로 객체를 받고, 그걸로 변수 초기화” 정도로 보는 게 맞아.

    return 0;
}