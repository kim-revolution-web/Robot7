#include<iostream>
using namespace std;

class Cat{


    public:
    Cat(){
        cout <<"객체가 생성되었습니다"<< endl;
    }
    ~Cat(){
        cout<<"객체가 소멸되었습니다!!!"<<endl;
    }

};

int main(){

    Cat tom;
    Cat jack;
    return 0;
}