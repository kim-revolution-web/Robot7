#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Weapon{
    protected:
    int level;
    string name;

    public:
    Weapon(){
        level =1;
        name ="무기";
    }


    virtual void attack(){
        cout <<"무기로 공격하다!"<<endl;
    }
    void showLevel(){
        cout <<"levle: "<<level<<endl;
    }
    void showName(){
        cout <<"name: "<<name<<endl;
    }
};
class Sword:public Weapon{
    public:
    Sword(){
        level =5;
        name="칼";
    }
     void attack()override{
        cout <<name<<"로 공격하다!"<<endl;
    }

};
class Axe:public Weapon{
    public:
    Axe(){
        level =10;
        name="도끼";
    }
     void attack()override{
        cout <<name<<"로 공격하다!"<<endl;
    }

};


int main()
{
    Weapon* weapon=new Weapon;
    weapon->attack();
    weapon->showLevel();
    weapon->showName();
    delete weapon;

    unique_ptr<Sword> sword =make_unique<Sword>();
    sword->attack();
    sword->showLevel();
    sword->showName();

    unique_ptr<Axe> axe =make_unique<Axe>();
    axe->attack();
    axe->showLevel();
    axe->showName();



    return 0;
}