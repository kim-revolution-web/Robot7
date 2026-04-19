#include <iostream>
#include <cstdlib>
using namespace std;


class Person{};
class Student : public Person{};
class StudenWorker : public Student{};

int main()
{
   StudenWorker gildong;

    return 0;
}