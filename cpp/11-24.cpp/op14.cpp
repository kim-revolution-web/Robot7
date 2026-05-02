#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class Hero
{
private:
    string treasure;

protected:
    int level;
    string name;

public:
    int mp;

    Hero()
    {
        treasure = "보물";
        level = 1;
        name = "영웅";
        mp = 10;
    }
    string getName()
    {
        return name;
    }
    string getTreasure()
    {
        return treasure;
    }
    int getLevel()
    {
        return level;
    }
};

class Wizard : public Hero
{
public:
    Wizard()
    {
        name = "마법사";
        level = 5;
    }
    void showLevel()
    {
        cout << level << endl;
    }
    void showName()
    {
        cout << name << endl;
    }
};

int main()
{
    unique_ptr<Hero> jack = make_unique<Hero>();
    cout << jack->getName() << endl;
    cout << jack->getLevel() << endl;

    unique_ptr<Wizard> geralt = make_unique<Wizard>(); // new로 만들어서
    geralt->showName();
    geralt->showLevel(); // 에로우 연산자로 해야함

    return 0;
}
