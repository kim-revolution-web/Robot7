#include <iostream>

using namespace std;
class Car
{

public:
    // 1.멤버변수
    int speed;
    string brand;
    string color;
    // 2.생성자
    Car():speed(0), brand("현대"),color("화이트"){}
    // Car() // defalut 생성자. 생성자 하나도 없으며 컴파일러가 자동으로 생성
    // {
    //     speed =0;
    //     brand = "현대";
    //     color = "화이트";
    // }

    // 3.멤버메소드
   string run()
    {
        //cout << "달리다~~!!" << endl;
        return "달리다~~!!";
    }
};

int main()
{

    Car myCar;
    cout << "myCar.speed :" << myCar.speed << endl;
    cout << "myCar.brand :" << myCar.brand << endl;
    cout << "myCar.color :" << myCar.color << endl;
    cout << "myCar.color :" << myCar.run() << endl;

    return 0;
}