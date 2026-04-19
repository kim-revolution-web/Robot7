#include <iostream>
#include <cstdlib>
#include <memory>
#include <string>

using namespace std;

class MagicStrategy
{
public:
    virtual void cast(const string &target) = 0;

    virtual ~MagicStrategy() = default;
};

class Fire_Magic : public MagicStrategy
{
public:
    virtual void cast(const string &target) override
    {
        cout << "화염 마법" << endl;
    }
};

class Ice_Magic : public MagicStrategy
{
public:
    virtual void cast(const string &target) override
    {
        cout << "얼음 마법" << endl;
    }
};

class Harry
{
public:
    MagicStrategy *currentMagic; // unique_ptr<MagicStrategy>
    Harry() : currentMagic(nullptr)
    {
    }
    void setMagic(MagicStrategy *magic)
    {
        currentMagic = magic;
        cout<<"[시스템]해리가 마법 준비중"<<endl;
    }
    void attack(const string &target)
    {
        if (currentMagic == nullptr)
        {
            cout << "[시스템] 아직 마법을 선택하지 않았습니다!\n";
            return;
        }
        currentMagic->cast(target);
    }
};
int main()
{
    Harry harry;
    Fire_Magic fire;
    Ice_Magic ice;

    string target = "볼트모트";
int choice;
       
    while(1){
         cout << "=== 해리 포터 마법 전투 시뮬레이터 ===\n";
        cout << "1. 화염 마법 선택\n";
        cout << "2. 얼음 마법 선택\n";
        cout << "3. 공격 실행\n";
        cout << "0. 종료\n";
        cout << "메뉴 선택 : ";
        cin >> choice;

        if(choice==0){
            cout <<"[시스템]전투를 종료합니다.\n";
            break;  
        }

         switch (choice)
        {
        case 1:
            harry.setMagic(&fire);
            cout << "[시스템] 해리가 화염 마법을 준비합니다.\n";
            break;

        case 2:
            harry.setMagic(&ice);
            cout << "[시스템] 해리가 얼음 마법을 준비합니다.\n";
            break;

        case 3:
            harry.attack(target);   // ✅ 문자열 전달
            break;

        default:
            cout << "[시스템] 잘못된 메뉴입니다. 다시 선택하세요.\n";
            break;
        }
    }

    return 0;
}