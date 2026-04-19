#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class Student
{

private:
    string name;
    int age;
    string major;
    int id;
    // 생성자를 private로
    Student(const string &name, int age, const string &major, int id)

        : name(name), age(age), major(major), id(id){}
public:
    class Builder
    {
       
    private:
        string name = "jack";
        int age = 36;
        string major = "computer";
        int id = 345345;

    public:
        // Builder(const string &name)
        //     : name(name) {}

        Builder &setName(const string &name)
        {
            this->name = name;
            return *this;
        }
        Builder &setAge(int age)
        {
            this->age = age;
            return *this;
        }
        Builder &setMajor(const string &major)
        {
            this->major = major;
            return *this;
        }
        Builder &setId(int id)
        {
            this->id = id;
            return *this;
        }
         Student build()
    {
        return Student(name, age, major, id);
    }
    };
    // 멤버
    // setter, getter
    string getName() { return name; }
    int getAge() { return age; }
    string getMajor() { return major; }
    int getId() { return id; }
   

};

int main()
{
    Student student = Student::Builder()
                          .setName("홍길동")
                          .setAge(20)
                          .setMajor("Embedded System")
                          .setId(20251234)
                          .build();

    cout << "Student Info\n";
    cout << "Name:  " << student.getName() << endl;
    cout << "Age:   " << student.getAge() << endl;
    cout << "Major: " << student.getMajor() << endl;
    cout << "ID:    " << student.getId() << endl;

    return 0;
}
