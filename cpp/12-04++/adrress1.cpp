
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <memory>
using namespace std;

class Person

{

private:
    int id;
    string name;
    string pnumber;

public:
    // 생성자
    Person() : id(0), name("아무개"), pnumber("010-1234-1234") {}
    Person(int id, string name, string pnumber) : id(id), name(name), pnumber(pnumber) {}
    // 소멸자
    // getter,setter
    int getId()
    {
        return id;
    }

    string getName()
    {
        return name;
    }
    string getPnumber()
    {
        return pnumber;
    }
};

int main()
{
    vector<Person> addressbook;
    auto person = make_unique<Person>(1, "홍길동", "010-1123-2324");
    addressbook.push_back(*person);
    person = make_unique<Person>(2, "이순신", "010-1234-2324");
    addressbook.push_back(*person);
    person = make_unique<Person>(3, "강감찬", "010-4567-2324");
    addressbook.push_back(*person);

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

        switch (select)

        {
        case 1:
        {
            // 주소록 조회 코드를 작성합니다.
            for (Person p : addressbook)
            {
                cout << "ID : " << p.getId() << " / ";
                cout << "이름 : " << p.getName() << " / ";
                cout << "전화번호 : " << p.getPnumber() << endl;
            }
            break;
        }
        case 2:
        {
            int n_id = 0;
            string n_name = "";
            string n_pnumber = "";

            cout << "새 ID 입력 : ";
            cin >> n_id;
            cout << "새 아름 입력 : ";
            cin >> n_name;
            cout << "새 전화번호 입력 : ";
            cin >> n_pnumber;

            auto p = make_unique<Person>(n_id, n_name, n_pnumber);
            addressbook.push_back(*p);
            // 주소록 추가 코드를 작성합니다.
            break;
        }

        case 5:
        {
            exit(1);
            break;
        }
        }
    }while (select != 0);
            
    
    return 0;
}
