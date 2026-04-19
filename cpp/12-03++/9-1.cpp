#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;
class Parent{
    public:
   virtual void f(){cout<<"Parent::f()"<<endl;}
};
class Child:public Parent{
    public:
    void f()override{cout<<"Child::f()"<<endl;}
};


int main()
{
    unique_ptr<Child> child= make_unique<Child>();
    child->f();
    // Derived d, *pDer;
    // pDer=&d;
    // pDer->f();
 unique_ptr<Parent> parent= make_unique<Child>();
    parent->f();
    // Base* pBase;
    // pBase = pDer;
    // pBase->f();

    return 0;
}