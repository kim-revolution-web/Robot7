#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>

using namespace std;

class Hero
{
public:
virtual void attack(){
    cout<<"영웅 공격하다~!"<<endl;
}
};

class knight:public Hero
{
public:
void attack() override{
    cout<<"기사 공격하다~!"<<endl;
}
};
      
class Archer:public Hero
{
public:
void attack() override{
    cout<<"궁수 공격하다~!"<<endl;
}
};
class Wizard:public Hero    
{
public:
void attack() override{
    cout<<"마법사 공격하다~!"<<endl;
}
};

int main()
{
    vector<unique_ptr<Hero>> heroes;
    heroes.push_back(make_unique<Hero>());
    heroes.push_back(make_unique<knight>());
    heroes.push_back(make_unique<Archer>());
    heroes.push_back(make_unique<Wizard>());

    for (const auto& hero : heroes) {
        hero->attack();
    }

    return 0;
}