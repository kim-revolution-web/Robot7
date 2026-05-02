#include <iostream>
#include <memory>
using namespace std;

class Dog {
public:
    unique_ptr<int> age;

    // 일반 생성자
    Dog(int a) : age(make_unique<int>(a)) {}

    // 복사 생성자 (깊은 복사)
    Dog(const Dog& other) : age(make_unique<int>(*other.age)) {}

    // 복사 대입 연산자 (깊은 복사)
    Dog& operator=(const Dog& other) {
        if (this != &other) {
            age = make_unique<int>(*other.age);
        }
        return *this;
    }
};

int main() {
    Dog d1(3);
    Dog d2 = d1;   // 복사 생성자

    *d2.age = 10;

    cout << "d1 age: " << *d1.age << '\n';
    cout << "d2 age: " << *d2.age << '\n';

    return 0;
}
