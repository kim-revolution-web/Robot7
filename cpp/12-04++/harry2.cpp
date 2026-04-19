#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;
// 기사 ,다크 나이트를 만들고
//  캐릭터 이름을 주고 캐릭털 기사 ,다크나이트의 함수 공격을 사용
// 이런식이 전략적? 패턴?

class Knight
{
    // 추상 클래스
public:
    virtual void skill() = 0;
    virtual ~Knight() = default;
};

class DarkKnight : public Knight
{
    virtual void skill() override
    {
        cout << "검은 검" << endl;
    }
};
class WhiteKnight : public Knight
{
    virtual void skill() override
    {
        cout << "하얀 검" << endl;
    }
};

class admin
{
private:
    Knight *adid;

public:
admin() : adid(nullptr){}
    void setskill(Knight *adid)
    {
        this->adid = adid;
    }
    void attack()
    {
        if (adid == nullptr)
        {
            cout << "스킬이 없다" << endl;
        }
        else
        {
            adid->skill();
        }
    }
};
int main()
{
    admin ad;
    DarkKnight DK;
    WhiteKnight WK;
    ad.setskill(&DK);
    ad.attack();

    ad.setskill(&WK);
    ad.attack();

    return 0;
}