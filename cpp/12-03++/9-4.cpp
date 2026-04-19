#include <iostream>
#include <memory>
using namespace std;

class Shape{
public:
    virtual void draw() {
        cout << "도형을 그리다" << endl;
    }
};
class Circle : public Shape{
public:
    void draw() override {
        cout << "원을 그리다" << endl;
    }
};
class Rect : public Shape{
public:
    void draw() override {
        cout << "사각형을 그리다" << endl;
    }
};
class Line : public Shape{
public:
    void draw() override {
        cout << "선을 그리다" << endl;
    }
};

int main()
{
    Shape*s = new Circle();
    s->draw();
    s->Shape::draw();

    delete s;
    return 0;
};
