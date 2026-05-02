#include <iostream>
#include <vector>
#include <string>

// vector<Dog> = Dog 객체 여러 개 저장
// push_back() = 뒤에 추가
// const auto& dog = 복사 없이 하나씩 읽기
class Dog {
public:
    std::string name;
    int age;

    Dog(std::string n, int a) : name(n), age(a) {}
};

int main() {
    std::vector<Dog> dogs;
    dogs.push_back(Dog("Choco", 3));
    dogs.push_back(Dog("Bori", 2));
    dogs.push_back(Dog("Coco", 1));

    for (const auto& dog : dogs) {
        std::cout << "name: " << dog.name << ", age: " << dog.age << '\n';
    }

    return 0;
  }
