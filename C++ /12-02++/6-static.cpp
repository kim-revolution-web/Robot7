#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Person{
    public:
    int money=1;

    void addMoney(int money){
        this->money+=money;
    }
    static inline int sharedMoney;
    static void addShardeMoney(int n){
        sharedMoney+=n;
    }
};

//int Person::sharedMoney=10; //외부 선언이 없으면 링크 오류
int main()
{
Person p1;
cout <<p1.sharedMoney<<":"<<p1.money<<endl;
cout <<p1.addMoney(100)<<":"<<p1.addShardeMoney<<endl;
Person p2;
cout <<p2.sharedMoney<<":"<<p2.money<<endl;
cout <<p2.addMoney(100)<<":"<<p2.addShardeMoney<<endl; 
    return 0;
}