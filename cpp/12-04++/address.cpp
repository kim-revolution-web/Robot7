#include <iostream>
#include <cstdlib>
#include <memory>
#include <vector>

using namespace std;

class Person
{
private:
    int id;
    string number;
    string pnumber;

public:
    Person(int id, string number, string pnumber) : id(id), number(number), pnumber(pnumber) {}

    // void setId(int id){this->id=id;}

    int getId()
    {
        return this->id;
    }
    string getNumber()
    {
        return this->number;
    }
    string getPnumber()
    {
        return this->pnumber;
    }
};
int main()
{
    vector<Person> address;
    unique_ptr<Person> p =
        make_unique<Person>(1, "홍길동", "010-1234-1234");
    address.push_back(*p);
    p = make_unique<Person>(2, "이순신", "010-4321-9876");
    address.push_back(*p);

    int select = -1;
    do
    {
        cout << "---------------------------------------------------------------- -" << endl;
        cout << "1. 주소록 조회" << endl;
        cout << "2. 주소록 추가" << endl;
        cout << "3. 주소록 수정" << endl;
        cout << "4. 주소록 삭제" << endl;
        cout << "5. 종료" << endl;
        cout << " 메뉴 : ";
        cin >> select;

        int id=0;
        string name="";
        string pnumber="";

        switch (select)
        {
        case 1:
        {
            for(Person p : address){
                cout<<"id:"<<p.getId()<<"/";
                cout<<"이름:"<<p.getNumber()<<"/";
                cout<<"전화번호:"<<p.getPnumber()<<"/";
            }
            break;
        }
            // 주소록 조회 코드를 작성합니다.

        case 2:
        
        { cout<<"새 ID 입력:";
            cin>>id;
            cout<<"새 이름 입력";
        cin>>name;
        cout<<"새 전화번호";
        cin>>pnumber;

        auto p = make_unique<Person>(id,name,pnumber);
        address.push_back(*p);
        
            // 주소록 추가 코드를 작성합니다.
            break;
        }
        case 5:
        {
            exit(1);
            break;
        }
        }

    } while (select != 0);

    return 0;
}