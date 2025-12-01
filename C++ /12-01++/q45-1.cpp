#include <iostream>
#include <memory>
using namespace std;

class Calculator
{
private:
    int a;
    int b;

public:
    void inputTwoNumbers()
    {
        cout << "두 수를 입력하세요:" << endl;
        cin >> a >> b;   // 멤버 변수에 직접 입력
    }

    int plus()
    {
        return a + b;
    }

    int minus()
    {
        return a - b;
    }

    int multiple()
    {
        return a * b;
    }

    double divide()
    {
        return static_cast<double>(a) / b;
    }
};

int main()
{
    // unique_ptr로 동적 생성 (new, delete 직접 사용 X)
    unique_ptr<Calculator> cal = make_unique<Calculator>();

    cal->inputTwoNumbers();

    cout << "plus : " << cal->plus() << endl;
    cout << "minus : " << cal->minus() << endl;
    cout << "multiple : " << cal->multiple() << endl;
    cout << "divide : " << cal->divide() << endl;

    return 0;
}