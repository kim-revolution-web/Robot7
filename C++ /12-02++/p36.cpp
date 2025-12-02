#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Person{
    public:
    int money; //개인 소유의 돈
    void addMoney(int money){
        this->money+=money;
    }
    static inline int sharedMoney=10; //공금
    static void addSharde(int n){
        sharedMoney+=n;
    }
};

// static 변수 생성. 전역 공간에 생성
//int Person::sharedMoney=10; //외부 선언이 없으면 링크 오류

int main()
{
Person::addSharde(50);
cout<<Person::sharedMoney<<endl;

Person han;
han.money=100;
han.sharedMoney=200;
Person::sharedMoney=300;
Person::addSharde(100);
cout<<han.money<<":"<<Person::sharedMoney<<endl;
cout<<Person::addSharde<<endl;
 
    return 0;
}