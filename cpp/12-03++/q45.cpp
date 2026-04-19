#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>

using namespace std;

class Hero{
    public:
   virtual void attack(){cout<<"Hero Attack~!"<<endl;}
};
class Warrior:public Hero{
    public:
    void attack()override{cout<<"Hero Attack~!"<<endl;}
};
class Knight:public Hero{
    public:
    void attack()override{cout<<"Hero Attack~!"<<endl;}
};
class Archer:public Hero{
    public:
    void attack()override{cout<<"Hero Attack~!"<<endl;}
};

int main()
{
    vector<Hero*>hero_list;// stack 영역에 개체
unique_ptr<Hero> k= make_unique<Knight>();// 객체가 heap 영에 생성
unique_ptr<Hero> w= make_unique<Warrior>();//a변수 stack a변수의 값이 주소 Archer객체가 있는 시작 주소
unique_ptr<Hero> a= make_unique<Archer>();
    hero_list.push_back(k.get());
    hero_list.push_back(w.get());
    hero_list.push_back(a.get());

    for(auto hero :hero_list){
        hero->attack();
    }
    return 0;
}