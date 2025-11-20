#include <iostream>

using namespace std;

class PrivateAccessError
{
private:
    int a;
    void f();
    PrivateAccessError();//구현해야 함 !!

public:
    int b;
    PrivateAccessError(int x); //구현해야함 !!
    void g();
};

PrivateAccessError::PrivateAccessError(){

    a=1;
    b=1;

}
PrivateAccessError::PrivateAccessError(int x){

    a=x;
    b=x;

}
void PrivateAccessError::f(){
    a=5;
    b=5;
}

void PrivateAccessError::g(){
    a=6;
    b=6;
}

int main()
{
    //PrivateAccessError objA; //Error
    PrivateAccessError objB(100);
    //objB.a = 10; //Error
    objB.b =20;
    //objB.f(); //Error 접근할 수 없다/ 보이지가 않는다.
    objB.g();

    return 0;
}