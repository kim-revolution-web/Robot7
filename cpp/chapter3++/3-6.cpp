#include <iostream>

using namespace std;

class Rectangle
{

public:
    int width;
    int height;
    // 생성자 3개 만들기

    Rectangle() : width(1), height(1) {};
    Rectangle(int length)
    {
        width = length;
        height = length;
    }
    Rectangle(int _width, int _height)
    {
        width = _width;
        height = _height;
    }
    // 함수 1개 만들기

    bool isSquare()
    {
        if (width == height)
            return true;
        else
            return false;
    }
};

int main()
{
    Rectangle rect1;
    Rectangle rect2(3, 5);
    Rectangle rect3(3);

    if (rect1.isSquare())
        cout << "rect1은 정사각형이다." << endl;
    if (rect2.isSquare())
        cout << "rect2은 정사각형이다." << endl;
    if (rect3.isSquare())
        cout << "rect3은 정사각형이다." << endl;

    return 0;
}