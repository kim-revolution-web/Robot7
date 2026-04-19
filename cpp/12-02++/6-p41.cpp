#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Person{
    int money;
    public:
    
     //static 멤머는 non-static 멤버에 접근할 수없음
    void setMoney(int money){
        this->money=money;
    }
    int getMoney(){return money;}
    static inline int static_money=1;
    static int sgetMoney(){return static_money;}

};
int main()
{
   cout<<Person::sgetMoney()<<endl;

    Person errorKim;
    errorKim.setMoney(100);
    cout<< errorKim.getMoney()<<endl;

    return 0;
}