#include <iostream>
#include <cstdlib>
#include <memory>
#include <vector>

using namespace std;

class Account
{
private:
    int id;
    string name;
    int blance;

public:
    Account(int id,const string &name, int initialBlance = 0)
    {
        this->id = id;
        this->name = name;
        this->blance = initialBlance;

    }
  
    int getId() const
    {
        return id;
    };

    string getName() const
    {
        return name;
    };

    int getBalance() const
    {
        return blance;
    };

    bool deposit(int amount)
    {
        if (amount > 0)
        {
            blance += amount;
            return blance;
        }
    };

    bool withdraw(int amount)
    {
        if (amount > 0 && amount <= blance)
        {
            blance -= amount;
            return blance;
        }
        else
        {
            cout << "잔액이 부족합니다." << endl;
            return false;
        }
    };
    void printInfo() const
    {
        cout << "계좌ID: " << id << ", 이름: " << name << ", 잔액: " << blance << endl;
    };
};

int main()
{

    // 1. 계좌 생성
     Account acc1(1001,"홍길동", 50000);
     Account acc2(1002,"이순신", 30000);

    // 2. 입금/출금 테스트
    acc1.deposit(20000);  // 정상 입금
    acc2.withdraw(5000);  // 정상 출금
    acc2.withdraw(50000); // 실패 테스트 (잔액 부족)

    // 3. 계좌 정보 출력
    acc1.printInfo();
    acc2.printInfo();

    // 4. vector로 여러 계좌 관리
    vector <Account> v;
    v.push_back(acc1);
    v.push_back(acc2);

     cout << "\n=== 전체 계좌 목록 ===\n";
    for (const auto &acc : v)
     {
         acc.printInfo();
    }

    return 0;
}
