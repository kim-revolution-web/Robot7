#include <iostream>
using namespace std;

class Cat
{

private:
    string eat;
    string color;
    int size;

public:
    Cat() {};                                                                             // 고정 맴버
    Cat(string _eat, string _color, int _size) : eat(_eat), color(_color), size(_size) {} // 생성자 변수 초기화

    void getEat(string _eat)
    {
        eat = _eat;
    }

    void getcolor(string _color)
    {
        color = _color;
    }

    void getsize(int _size)
    {
        size = _size;
    }

    string puEat()
    {
        return eat;
    }

    string pucolor()
    {
        return color;
    }

    int pusize()
    {
        return size;
    }
};

int main()
{

    Cat riri;
    Cat nongnong("고등어", "빨강", 30);
    Cat *ningning = new Cat;
    ningning->getsize(23);
    cout << "ningning 사이즈" << ningning->pusize() << endl;

    delete ningning;

    return 0;
}