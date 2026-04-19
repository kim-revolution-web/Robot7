#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class MagicStrategy
{ // 추상 클래스
public:
    virtual void cast() = 0;            // 순수 가상 함수
    virtual ~MagicStrategy() = default; // 부모 클래스의 소멸자 실행되고 자식 클래스의 소멸자
};

class FireMagic : public MagicStrategy
{
public:
    void cast() override
    { // 순수 가상함수는 자식 클래스에 강제로 구현해야 한다 !!
        cout << "화염 마법 선택" << endl;
    }
};

class Harry
{
private:
    MagicStrategy *starategy; // 포인터 선언
public:
    void setMagicStrategy(MagicStrategy *starategy)
    {
        this->starategy = starategy;
    }
    void attack()
    {
        if (starategy == nullptr)
        {
            cout << "현재 선택된 마법이 없습니다. 마법을 먼저 선택하세요." << endl;
            return;
        }
        starategy->cast();
    }
};
int main()
{
    Harry harry;
    FireMagic fireMagic;
    harry.setMagicStrategy(&fireMagic);
    harry.attack();

    return 0;
}