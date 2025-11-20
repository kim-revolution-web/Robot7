#include <iostream>
#include <memory>

using namespace std;

class Cat
{
private:
    int age;
    string name;
    string type;

public:
    // 생성자
    Cat() {} // 디퐅트 생성자
    Cat(int _age, string _name, string _type)
        : age(0), name("고양이"), type("랙돌")
    {
    }

    void setAge(int _age)
    {
        age = _age;
    }

    void setName(string _name)
    {
        name = _name;
    }

    void setType(string _type)
    {
        type = _type;
    }

    int getAge()
    {
        return age;
    }
    string getName()
    {
        return name;
    }
    string getType()
    {
        return type;
    }
};

int main()
{

    Cat tom;
    Cat *marry = new Cat();
    marry->setName("메리");
    cout << "메리 고양이의 이름은 :" << marry->getName() << endl;

    delete marry;
    return 0;
}